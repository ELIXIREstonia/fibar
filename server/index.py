from flask import Flask, Response, session, stream_with_context, request, render_template, jsonify, send_file
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import cv2
import fibar
import re
from io import BytesIO
import shutil
import base64
import sys
import numpy as np
import hashlib
import secrets
import pandas as pd
from zipfile import ZipFile

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
# this path should probably be changed
UPLOAD_FOLDER = 'server/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.tif']

def convert_np_ints(obj):
    if isinstance(obj, np.integer):  # Convert np.int64
        return int(obj)
    elif isinstance(obj, list):  # Apply recursively if list
        return [convert_np_ints(i) for i in obj]
    else:
        return obj


@app.route("/api/upload", methods=['POST'])
@cross_origin()
def upload_file():

    try:
         uploaded_files = request.files.getlist('image')
         id = secrets.token_hex(10//2)
         session_path = os.path.join(app.config['UPLOAD_FOLDER'], str(id))
         if not os.path.exists(session_path):
             os.makedirs(session_path)

         img_content_lst, filename_lst = [], []
         results = {}
         for uploaded_file in uploaded_files:

             filename = secure_filename(uploaded_file.filename)
             filepath = os.path.join(session_path, filename)

             # saving uploaded file to static folder 
             uploaded_file.save(filepath)

             # scales 
             value, unit, scale = fibar.scaling(filepath)
             results[filename] = {
                 "file_path": filepath,
                 "number": str(value),
                 "unit": unit,
                 "scale": str(scale), 

             }

         return jsonify({
             "status": "ok",
             "upload_id": str(id),
             "data": results

         })


    except Exception as e:
        return {
        "status": "err",
        "message": str(e),
        }


@app.route("/api/analyze", methods=['GET', 'POST'])
@cross_origin()
def analyze_file():

    print("analyse", flush=True)
    print("content", request.json, flush=True)
    content = request.json

    parent_folder=os.path.join(app.config['UPLOAD_FOLDER'], content["folder_id"])
    output_folder=os.path.join(parent_folder, "output")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    results = {}
    integer_value = int(content["measurements_no"]) # measurements
    files_only = [f for f in os.listdir(parent_folder) if os.path.isfile(os.path.join(parent_folder, f)) ]
    rows, output_files = [], []

    for file_path in files_only:
        if not file_path.endswith("zip"):

            full_file_path = os.path.join(parent_folder, file_path)

            unit = content["value_unit_scale_dict"][file_path]["unit"]

            try:
                value = int(content["value_unit_scale_dict"][file_path]["number"])
                scale = int(content["value_unit_scale_dict"][file_path]["scale"])

            except:
                value, scale  = None, None 


            unit_check, measurements, im_array, start_end_coords = fibar.measure_dm(full_file_path, integer_value, [value, unit, scale], False)
            start_end_coords = convert_np_ints(start_end_coords)
            output_file = os.path.join(output_folder, "{}.png".format(file_path.split(".")[0]))

            if unit_check: unit = "px"
            else: unit = "nm"

            # saving file to folder 
            cv2.imwrite(output_file, im_array)

            input_file_png = os.path.join(output_folder, "{}_input.png".format(file_path.split(".")[0]))
            cv2.imwrite(input_file_png, cv2.imread(full_file_path))

            rows.append([file_path, str(measurements), np.mean(measurements), np.std(measurements), np.median(measurements), unit])
            output_files.append(output_file)


            results[file_path] = {"measurements": measurements,
                                "mean": round(np.mean(measurements), 1),
                                "stdev": round(np.std(measurements), 1),
                                "median": round(np.median(measurements), 1),
                                "result_unit": unit,
                                "output_file_path": output_file,
                                "start_end_coords": start_end_coords, 
                                "input_file_png": input_file_png
                                }

    header_row =  ["File path", "Diameter measurements", "Mean", "Standard deviation", "Median", "Unit"]
    df = pd.DataFrame(rows, columns=header_row)

    archive = shutil.make_archive(f'{parent_folder}/measured_images', 'zip', output_folder)
    print("this is the zip file path ", archive)

    if os.path.exists(archive):
        os.remove(archive)
        archive = shutil.make_archive(f'{parent_folder}/measured_images', 'zip', output_folder)


    return jsonify({
        "status": "ok",
        "data" : results,
        "csv_table": df.to_csv(index=False),
        "zip_path": archive,
        })

@app.route("/api/results_update", methods=['GET', 'POST'])
@cross_origin()
def results_update():
    content = request.json

    parent_folder=os.path.join(app.config['UPLOAD_FOLDER'], content["folder_id"])
    output_folder=os.path.join(parent_folder, "output")
    results = {}

    received_results = content["results"] # expecting the old results dict
    new_coords = content["coords"] # expecting new coords
    value_unit_scale = content["value_unit_scale"]
    changed = content["changed"]
    #print("changed", changed)
    files_only = [f for f in os.listdir(parent_folder) if os.path.isfile(os.path.join(parent_folder, f)) ]
    rows, output_files = [], []
    print(list(received_results.keys()))
    # updating some values in the dictionary 
    for file_path in list(received_results.keys()):
        print(file_path)
        full_file_path = os.path.join(parent_folder, file_path)

        im_array, _ = fibar.drawer(full_file_path, new_coords[file_path], -1)
        output_file = os.path.join(output_folder, "{}.png".format(file_path.split(".")[0]))
        # saving input file as png 

        cv2.imwrite(output_file, im_array)
        new_measurements = received_results[file_path]["measurements"]

        if value_unit_scale[file_path]["result_unit"] == "nm" and changed[file_path] == True:
                # rescaling the measurements 
                tmp_measurements = new_measurements
                if value_unit_scale[file_path]["unit"] == "um":
                    new_measurements = list(1000 * ( (np.array(tmp_measurements) * int(value_unit_scale[file_path]["number"])) / int(value_unit_scale[file_path]["scale"])) )
                elif value_unit_scale[file_path]["unit"] == "nm":
                    new_measurements = list( (np.array(tmp_measurements) * int(value_unit_scale[file_path]["number"])) / int(value_unit_scale[file_path]["scale"])) 


        # rounding measurements down
        new_measurements = np.round(np.array(new_measurements), 2).tolist()

        rows.append([file_path, str(new_measurements), np.round(np.mean(new_measurements), 2), np.round(np.std(new_measurements), 2), np.round(np.median(new_measurements), 2), received_results[file_path]["result_unit"]])
        output_files.append(output_file)


        results[file_path] = {
            "measurements":new_measurements,
            "mean": round(np.mean(new_measurements), 1),
            "stdev": round(np.std(new_measurements), 1),
            "median": round(np.median(new_measurements), 1),
            "output_file_path": output_file, 
        }


    header_row =  ["File path", "Diameter measurements", "Mean", "Standard deviation", "Median", "Unit"]
    df = pd.DataFrame(rows, columns=header_row)

    archive = shutil.make_archive(f'{parent_folder}/measured_images', 'zip', output_folder)
    if os.path.exists(archive):
        os.remove(archive)
        archive = shutil.make_archive(f'{parent_folder}/measured_images', 'zip', output_folder)
    
    return jsonify({
    "status": "ok",
    "data" : results,
    "csv_table": df.to_csv(index=False),
    "zip_path": archive,
    })

@app.errorhandler(Exception)
def handle_errors(e):
    return {
        "status": "err",
        "message": str(e),
    }

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=9090)


