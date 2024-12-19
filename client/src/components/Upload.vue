<!-- ImageUploader.vue -->
<template>
    <div class="container-fluid">

      <div class="row">
        <div class="col-12 col-md-4">
        
      <label class="drop-area"
      :class="{ dragging: isDragging, 'disabled': DropAreaDisabled}"
      @dragover.prevent="handleDragOver"
      @dragenter.prevent="handleDragEnter"
      @dragleave="handleDragLeave"
      @drop.prevent="handleDrop">
        <p>Drag and drop files here, or click here to select files. <br>Accepted formats: TIF, PNG, JPG. Max file size: 2MB</p>
        <input
          type="file"
          ref="fileInput"
          @change="handleFileChange"
          style="display: none"
          multiple
        />
      </label>
    </div>

    <div class="col-8">
    <div class = "button-container">
      <div>
        <b-button 
        :disabled = "resultsAdded || error || upload_data!=null"
        :class="{'btn-load btn btn-outline-secondary btn-sm mr-2': !resultsAdded, 'btn-load-results btn btn-outline-success btn-sm mr-2': upload_data!=null}"
        @click="example_image('15k_example.tif')" v-b-modal.modalPopover>Load example image 1</b-button>
      </div>
      <div>

        <b-button 
        :disabled= "resultsAdded || error || upload_data!=null"
        :class="{'btn-load btn btn-outline-secondary btn-sm mr-2': !resultsAdded, 'btn-load-results btn btn-outline-success btn-sm mr-2': upload_data!=null }"
        @click="example_image('20k_example.tif')" v-b-modal.modalPopover>Load example image 2</b-button>
      </div>
      </div>
</div>
</div>
     <br>
      <div v-if="uploadedFiles.length > 0 && !showExample && !DropAreaDisabled">

        <h2>Files to be uploaded:</h2>
        <table>
          <thead>
          </thead>
          <tbody>
            <tr v-for="(file, index) in uploadedFiles" :key="index">
              <td>{{ file.name }}</td>
            </tr>
          </tbody>
        </table>
        <br>
        <b-button :style="{backgroundColor: '#4caf50'}" v-b-modal.modalPopover @click="uploadImages" :disabled="uploadedFiles.length === 0 || loaderinp">Upload</b-button>

      </div>

      <br>
      <div v-if="loaderinp" class="text-center">
            <div class="spinner-border text-primary spinner" role="status">
            </div>
            <p>Please wait. Input files are being validated.</p>
          </div>
          <transition name="fade"> </transition>

      <b-alert variant="danger" :show="!!error" @dismissed="clear" dismissible >{{ error }}</b-alert>


        <!-- <div v-if="result_data == null"> -->
        <div v-if=" upload_data != null && error==false">

        <h2 v-if="!resultsAdded">Input files</h2>

        <h2 v-else>Results</h2>

        <b-button @click="exportCsv" 
        :disabled="loader || !resultsAdded"
        :class="{'btn-custom btn btn-outline-secondary btn-sm mr-2': !resultsAdded, 'btn-custom-results btn btn-outline-success btn-sm mr-2': resultsAdded }">
                <i class="bi bi-file-earmark-spreadsheet"></i>
                Export CSV
            </b-button>

            <b-button  @click="exportImages" 
            :disabled="loader || !resultsAdded || loader_zip"
            :class="{'btn-custom btn btn-outline-secondary btn-sm mr-2': !resultsAdded , 'btn-custom-results btn btn-outline-success btn-sm mr-2': resultsAdded }">
                <i class="bi bi-file-earmark-image"></i>
                Export images with measurements
            </b-button>
            <br>

          <div v-if="loader" class="text-center">
            <div class="spinner-border text-primary spinner" role="status">
              <span class="sr-only"></span>
            </div>
            <p>Please wait. Results will occur soon.</p>
          </div>
          <transition name="fade"> </transition>

        <div class="table-container">
            <table border="1" :class="{'loading':loader}">
                <thead>
                <tr>
                 <th v-for="(column, index) in init_tableColumns" :key="index" :class="{'editable': 0 < index && index<3 && init_tableColumns.length<=3, 'not-editable': 0 < index && index<3 && init_tableColumns.length>3}">
                  {{column}}
                </th>
                </tr>
              </thead>
              <tbody>
              <tr v-for="(value, key) in upload_data" :key="key">
                <td> <a href="#" @click.prevent="showInpImage(value.file_path)" > {{key}} </a> </td>

                <td :contenteditable="!resultsAdded" @blur = "updateNumber(key, 'number')" > {{ value.number}}</td>

                <td>
                  <select v-model="value.unit" @change="updateUnit(key, 'unit')">
                  <option v-for="option in statusOptions" :key="option" :value="option" :disabled="resultsAdded" >{{ option }}</option>
                  </select>
                </td>

                <td v-if="resultsAdded"> {{ value.mean }}</td>
                <td v-if="resultsAdded"> {{ value.stdev }}</td>
                <td v-if="resultsAdded"> {{ value.median }}</td>
                <td v-if="resultsAdded"> {{ value.result_unit }}</td>
                <td v-if="resultsAdded">

                    <b-button :style="{backgroundColor: '#1F487E'}" v-b-modal.modalPopover @click="showPlot(value.measurements, value.result_unit); showImage(value.output_file_path); prepDraw(value.input_file_png, key)">Show results</b-button>
                </td>
              </tr>
          </tbody>
            </table>
            <br>
            
            <b-alert variant="danger":show="!!error" @dismissed="clear">{{error}}
            </b-alert>

            <b-alert show variant="info" :show="!!warning1" dismissible> {{ warning1 }}</b-alert>
            <b-alert show variant="warning" :show="!!warning3" dismissible> {{ warning3 }}</b-alert>
            <b-alert show variant="warning" :show="!!warning2" dismissible> {{ warning2 }}</b-alert>



            
            <b-modal v-model="showModalInp" title="Input image" class="input-modal" ok-only size="xl" @hidden="">
              <div class="modal-content" style="display:flex; justify-content: center; width: 100%; max-height: 100%; overflow: auto;">
            <img :src="imageSrc" alt="Input image"  width="60%" height="60%" >
          </div>
            </b-modal>

            <b-modal id="results" v-model="showModal" title="Results" @hidden="clearPlot" centered class="custom-modal" ref="myModal" size="xl" ok-only>
                    <b-tabs content-class="mt-3" v-model="activeTab">
                        <b-tab title = "Histogram" active>
                          <div style="display:flex; justify-content: center; width: 100%; max-height: 100%; overflow: auto;">
                                <Plotly v-if="showPlotComponent" :data="data" :layout="layout" :config="plotConfig"></Plotly>
                            </div>
                        </b-tab>

                          <b-tab title="Measurements" @click = "draw">
                            <p> <b>Edit</b> the lines by pulling the red endpoints. <b>For deletion,</b> click on the center ("X") part of the line. <b>To add a new line</b> double click on desired region in the image. <b>If you are satisfied with the measurements, </b> click on "Save changes". The image with the measurements (without "X"-s) will be updated as well as the data in the table and CSV.</p>

                           <div style="display:flex; justify-content: center; width: 100%; max-height: 100%;overflow: auto">
                              <canvas
                                ref="canvas"
                                @mousedown="startDrag"
                                @mousemove="drag"
                                @mouseup="endDrag"
                                @dblclick="addLine"
                                
                                style="border: 1px solid black" 
                              ></canvas>
                              </div>
                          
                                <br>



                        </b-tab>
                    </b-tabs>
                    <template v-slot:modal-footer>
                      <div v-if="activeTab === 1" class="d-flex justify-content-between align-items-center px-3 w-100">
                        <p class="mb-0">No. of measurements: {{ lines[original_key].length }}</p>
                        <b-button variant="primary" @click="saveButton">Save changes</b-button>
                    </div>
                    </template>
                </b-modal>
          </div>

        <br>
        <label for="userInput">Number of diameter measurements:</label>
        <input
          type="number"
          id="userInput"
          v-model="userNumber"
          :min="minNumber"
          :max="maxNumber"
          :disabled="loader"href
        />

      <b-button :style="{backgroundColor: '#1F487E'}" v-b-modal.modalPopover @click="analyzeImages"  :disabled="loader" >Analyze</b-button>
      <b-button :style="{borderColor: '#4caf50', backgroundColor: 'white', color: '#4caf50'}" v-b-modal.modalPopover @click="clear" :disabled="loader">Upload new image(s)</b-button>
        </div>
      </div>
  </template>

  <script>
  import API from '../api';
  import Analysis from "@/components/Analysis";
  import HGtest from "@/components/HGtest"
  import { Plotly, full } from 'vue-plotly';
  import { saveAs } from 'file-saver';
  import _ from 'lodash';
  import { BIconThreeDotsVertical, BModal } from 'bootstrap-vue';
  import Tiff from 'tiff.js';




  function formatDate(date) {
      var hours = date.getHours();
      var minutes = date.getMinutes();
      var seconds = date.getSeconds();
      //hours = hours % 12;
      //hours = hours ? hours : 12; // the hour '0' should be '12'
      minutes = minutes < 10 ? '0'+minutes : minutes;
      seconds = seconds < 10 ? '0'+seconds : seconds;
      var strTime = hours + '-' + minutes + '-' + seconds;

      var month = (date.getMonth()+1);
      month = month < 10 ? '0'+month : month;

      var day = date.getDate();
      day = day < 10 ? '0'+day : day;

      return date.getFullYear() + "-" + month + "-" + day + "_" + strTime;
  }

  function pathCorrecter(path){
    if (path.startsWith("/opt")) { 
      return API.baseURL+_.join(_.split(path, "/").slice(3), "/")
    }
    return API.baseURL+_.join(_.split(path, "/").slice(1), "/")
  }

  function getIntegerAverage(arr) {
    if (arr.length === 0) return 0; // Handle empty array case
    
    const sum = arr.reduce((acc, val) => acc + val, 0);
    const average = sum / arr.length;

    return Math.round(average); // Rounds to the nearest integer
  }

  export default {
    components: {
        Analysis, HGtest, Plotly, BModal
    },
    data() {
      return {
        uploadedFiles: [],
        progress: 0,
        error: false, 
        warning1: "",
        warning2: "",
        warning3: "",
        isDragging: false,
        isHidden: false,
        userNumber: 100, // Initial value for user input
        minNumber: 1, // Minimum allowed value
        maxNumber: 1000, // Maximum allowed value
        user_hash: 0,
        result_data: null,
        loader: false,
        loaderinp: false,
        pixelConv: false,
        imageUrl: [],
        viewImage: null,
        upload_data: null,
        upload_data_cp: null,
        statusOptions: ["um", "nm", "None", "px"],
        defaultStatus: "um",
        resultsAdded: false,
        init_tableColumns: ["File name", "Scale value", "Scale unit"],
        result_tableColumns: ["Mean", "Standard deviation", "Median", "Results in units", "Result visuals"],
        showModal: false,
        showExample: false,
        showPlotComponent: false,
        DropAreaDisabled: false,
        outimagePath: "",
        imagePath:"",
        imageSrc: "",
        showModalInp: false,
        activeTab: 0,
        input_file: null,
        original_key:"",
        scaleFactor: 1,
        changed: {},
        loader_zip: false,
        coordinates: {},
        lines: {},
        isLineDragging: false,
        dragPointType: null, // Can be 'start', 'end' for dragging a line endpoint
        selectedLineIndex: null,
        showX: false,
        data: [{
            x: [],
            type: 'histogram',
        }],

        layout: {
            xaxis: {title:'Measurements '}, 
            yaxis: {title: 'Frequency'},
            autosize: true,
            margin: { l: 50, r: 50, b: 50, t: 50, pad: 4 },
        },

        plotConfig: {
            displayModeBar: false,
            responsive: true
        },

      };
    },
    computed: {
      formattedPercentage() {
      return `${(this.scaleFactor * 100)}%`
      }
    },


    methods: {

      saveButton() {
        this.saveChanges()
        this.closeModal()
      },

      closeModal() {
        this.$bvModal.hide("results")
      },

      handleDragOver(event) {
        event.preventDefault();
        this.isDragging = true;
      },
      handleDragEnter(event) {
        event.preventDefault();
        this.isDragging = true;disabled
      },
      handleDragLeave() {
        this.isDragging = false;
      },
      handleDrop(event) {
        event.preventDefault();
        this.isDragging = false;

        const files = event.dataTransfer.files;
        this.handleFiles(files);
      },

      handleFileChange() {
        const fileInput = this.$refs.fileInput;
        const files = fileInput.files;
        this.handleFiles(files);
      },
      handleFiles(files) {
        this.uploadedFiles = this.uploadedFiles.concat(Array.from(files));
      },

      updateNumber(file, key) {
        this.upload_data[file][key] = event.target.innerText
      },

      updateUnit(file, key) {
        this.upload_data[file][key] = this.upload_data[file][key]
      },


      draw() { 

        const canvas = this.$refs.canvas;
        const ctx = canvas.getContext("2d");

        // Clear the canvas before each draw to prevent duplicate points/lines
        const image = new Image();

        image.src = this.input_file
        
        image.onload = () => {


          const canvas_padding = 20

          // Set canvas size to match the image size
          canvas.width = image.width * this.scaleFactor;
          canvas.height = image.height *this.scaleFactor;

          ctx.drawImage(image, 0, 0, image.width* this.scaleFactor, image.height* this.scaleFactor); // Draw image
        // Draw all lines and their endpoints
        this.lines[this.original_key].forEach(line => {
          // Draw the line
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y);
          ctx.lineTo(line.end.x, line.end.y);
          ctx.strokeStyle = 'black';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Draw perpendicular lines at the start and end points
          this.drawPerpendicularLine(ctx, line.start, line.end, 10); 
          this.drawPerpendicularLine(ctx, line.end, line.start, 10); 

          if (line.length > 15) {
          this.drawX(ctx, Math.floor((line.start.x + line.end.x) / 2), Math.floor((line.start.y + line.end.y) / 2));
          }
        
        });
        }
        },

        drawPerpendicularLine(ctx, start, end, length) {
          // Calculate the direction vector (from start to end)
          const dx = end.x - start.x;
          const dy = end.y - start.y;

          // Normalize the direction vector to get a unit vector
          const magnitude = Math.sqrt(dx * dx + dy * dy);
          const ux = dx / magnitude;
          const uy = dy / magnitude;

          // Calculate the perpendicular vector by swapping x and y, and negating one component
          const perpX = -uy;  // Perpendicular to (ux, uy)
          const perpY = ux;

          // Determine the start and end points for the perpendicular line
          const perpStartX = start.x - perpX * length / 2;
          const perpStartY = start.y - perpY * length / 2;
          const perpEndX = start.x + perpX * length / 2;
          const perpEndY = start.y + perpY * length / 2;

          // Draw the perpendicular line
          ctx.beginPath();
          ctx.moveTo(perpStartX, perpStartY);
          ctx.lineTo(perpEndX, perpEndY);
          ctx.strokeStyle = 'red';
          ctx.stroke();
      },

    calculateLineLength(start, end) {
      // Use Euclidean distance formula
      const dx = end.x - start.x;
      const dy = end.y - start.y;
      return Math.sqrt(dx * dx + dy * dy);
    },

    startDrag(event){
      const { offsetX, offsetY } = event;

      // Find which line's start or end point is being clicked
      this.selectedLineIndex = -1; // Default to -1 if not found
      for (let i = 0; i < this.lines[this.original_key].length; i++) {
        const line = this.lines[this.original_key][i];
        if (
          Math.hypot(line.start.x - offsetX, line.start.y - offsetY) < 10 ||
          Math.hypot(line.end.x - offsetX, line.end.y - offsetY) < 10
        ) {
          this.selectedLineIndex = i;
          break;
        }

      }

      // If a line's endpoint is clicked, determine if it's the start or end point
      if (this.selectedLineIndex !== -1) {
        const line = this.lines[this.original_key][this.selectedLineIndex];
        if (Math.hypot(line.start.x - offsetX, line.start.y - offsetY) < 10) {
          this.dragPointType = "start"; // Dragging the start point of the line
        } else if (Math.hypot(line.end.x - offsetX, line.end.y - offsetY) < 10) {
          this.dragPointType = "end"; // Dragging the end point of the line
        }
        this.isLineDragging = true;
      }

      let lineToDelete = -1;

      this.lines[this.original_key].forEach((line, index) => {
        const distanceToLine = this.calculateDistanceToLine({ x: offsetX, y: offsetY }, line.start, line.end);

        // Only consider deleting if the click is close to the line but not near the endpoints
        
        if (distanceToLine < 5 && line.length >= 15) {
          lineToDelete = index;
          }
        });

        // Delete the line if a valid click occurred near the middle part
        if (lineToDelete !== -1) {
          this.lines[this.original_key].splice(lineToDelete, 1);
          this.draw(); // Redraw the canvas after deletion
        }
    
    },

    drag(event) {
      const { offsetX, offsetY } = event;

      if (this.isLineDragging) {
        // Handle dragging logic
        if (this.dragPointType === "start" && this.selectedLineIndex !== null) {

          this.lines[this.original_key][this.selectedLineIndex].start.x = offsetX;
          this.lines[this.original_key][this.selectedLineIndex].start.y = offsetY;

        } else if (this.dragPointType === "end" && this.selectedLineIndex !== null) {
          this.lines[this.original_key][this.selectedLineIndex].end.x = offsetX;
          this.lines[this.original_key][this.selectedLineIndex].end.y = offsetY;
        }

        // Update line length
        this.lines[this.original_key][this.selectedLineIndex].length = this.calculateLineLength(
          this.lines[this.original_key][this.selectedLineIndex].start,
          this.lines[this.original_key][this.selectedLineIndex].end
        );

        // Redraw the canvas after dragging
        this.draw();
      }
      },

    addLine(event) {

      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext("2d");

      // Get the mouse position on double-click
      const rect = canvas.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      const lineLength = Math.floor(getIntegerAverage(this.lines[this.original_key].map(line => line.length))); // Constant length, can be adjusted
      const halfLength = Math.floor(lineLength / 2);

      // Calculate start and end points centered around the mouse position
      const start = { x: Math.floor(x - halfLength), y: Math.floor(y) };
      const end = { x: Math.floor(x + halfLength), y: Math.floor(y) };

      this.draw();

      this.lines[this.original_key].push({start, end, length: lineLength})
      
    },

    drawX(ctx, x, y) {
      const size = 5; // Size of the "X"
      ctx.beginPath();
      ctx.moveTo(x - size, y - size);
      ctx.lineTo(x + size, y + size);
      ctx.moveTo(x - size, y + size);
      ctx.lineTo(x + size, y - size);
      ctx.strokeStyle = "orange";
      ctx.lineWidth = 1;
      ctx.stroke();
    },

    calculateDistanceToLine(point, start, end) {
    // Calculate the distance from the point to the line segment defined by start and end
    // Implement the distance formula logic

    // Convert points to vector format: [x, y]
    const p1Vec = [start.x, start.y];
    const p2Vec = [end.x, end.y];
    
    // midpoint of the line
    const mVec = [Math.ceil((p1Vec[0] + p2Vec[0]) / 2), Math.ceil((p1Vec[1] + p2Vec[1]) / 2)]
    const pointImpVec = [point.x, point.y];

    // distance from midpoint
    var distance = this.calculateLineLength({ x: mVec[0], y: mVec[1] }, {x: pointImpVec[0], y: pointImpVec[1]})
    
    return distance;

  },

  endDrag()  {
      this.isLineDragging = false;
      this.dragPointType = null;
      this.selectedLineIndex = null;
    },

  updateCoordinates() {
    // Map over the lines array to create a new coordinates array
    this.coordinates[this.original_key] = this.lines[this.original_key].map(line => [
      [line.start.x, line.start.y], // Start coordinate
      [line.end.x, line.end.y]      // End coordinate
    ]);

  },

    saveChanges() {
      // update the coordinates array 
      this.updateCoordinates()

      this.changed[this.original_key] = true
      // updating and scaling before sending back 
      this.result_data.data[this.original_key]["start_end_coords"] = this.coordinates[this.original_key] 
      this.result_data.data[this.original_key]["measurements"] =this.lines[this.original_key].map(line => line.length)


      this.resultsUpdate()
    },

    popup(){
      this.showModalInp = true
    }, 


      uploadImages() {
        const formData = new FormData();
        const allowedFormats =  ["png", "tif", "tiff", "jpg"]; 
        const pattern = /(?:^|[\W_])\d{1,3}\s*(?:[kx]|kx).*?(?=[\W_]|$)/i;

        this.uploadedFiles.forEach((file) => {

          if ( allowedFormats.some(extension => file.name.endsWith(extension)))  {
              formData.append('image', file);
            }
          else {
            this.error = 
            "The image(s) is not of .PNG, .TIF(F), .JPG format. Check the User guide for more information.\nClick on 'x' to load new images."
          }
        
        });

        this.loaderinp = true
        API.upload(formData, (response) => 
        {
          if (response.status === "ok") {
            this.upload_data = response.data
            this.upload_data_cp = this.upload_data

            this.loaderinp = false
            this.DropAreaDisabled = true
            this.user_hash = response.upload_id
            this.warning1 = "Ensure that the detected number and unit match your input image."
            let noScaleFiles = []
            let missingValuesFiles = []
            

            Object.keys(this.upload_data).forEach(objKey => {

            if (this.upload_data[objKey].scale === "None") {
              this.upload_data[objKey].unit = "px";
              noScaleFiles.push(objKey);
            }

            else if (this.upload_data[objKey].number === "None" || this.upload_data[objKey].number == null ||
                    this.upload_data[objKey].unit === "None" || this.upload_data[objKey].unit == null) {
              missingValuesFiles.push(objKey);
            }
            });

                    
          // Construct the warnings based on files in the arrays
          if (noScaleFiles.length > 0) {
            this.warning2 = `The program could not detect a scale bar properly for ${noScaleFiles.join(', ')}, so the analysis will be done in pixels.`;
          }

          if (missingValuesFiles.length > 0) {
            this.warning3 = `The program could not detect the unit/number properly for ${missingValuesFiles.join(', ')}, please edit values in the according cells.`;
          }

          // Error message for upload failure
          if (Object.keys(this.upload_data).length === 0) {
            this.error = "Something went wrong when uploading the files. Try to refresh and re-upload the images. In case the issue persists, check the User guide.";
          }
            
        }})
      
      },

    analyzeImages() {

        this.result_data=null
        this.loader=true
        this.coordinates = {}
        this.lines = {}
        this.input_file = null
        this.changed = {}


        API.analyze({
            'folder_id':this.user_hash,
            'measurements_no': this.userNumber,
            'value_unit_scale_dict': this.upload_data,

        }, results  => {
            if (results.status === "ok") {

                // adding new columns to table
                if (!this.resultsAdded) {
                this.init_tableColumns.push(this.result_tableColumns)
                this.init_tableColumns= _.flattenDeep(this.init_tableColumns)
                }

                this.resultsAdded = true

                this.result_data = results

                Object.keys(this.result_data.data).forEach( objKey => 
                {
                  this.coordinates[objKey] = this.result_data.data[objKey]["start_end_coords"]//* this.scaleFactor
                  this.changed[objKey] = false
            
                })

              this.lines = Object.keys(this.coordinates).reduce((linesObj, fileName) => {
                  linesObj[fileName] = this.coordinates[fileName].map(pair => {
                          const start = { x: pair[0][0], y: pair[0][1] };
                          const end = { x: pair[1][0], y: pair[1][1] };
                          const length = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
                          return { start, end, length };
                      })
                  ;
                  return linesObj;
              }, {});
            
              this.upload_data = _.merge({}, this.upload_data_cp, this.result_data.data)
              this.loader = false;
          }
              else if (results.status === "err") {
                  this.error = results.message+"\n Something went wrong with the analysis. Try again by clicking on 'x'. If the issue persists, contact us."
              }
        })
    },

    resultsUpdate() {

    API.results_update({

        'folder_id':this.user_hash,
        'results': this.result_data.data,
        'coords': this.coordinates,
        'file_path': this.original_key,
        'value_unit_scale': this.upload_data,
        'changed': this.changed

        }
        
        , updated_results  => {
        if (updated_results.status === "ok") {

            // adding new columns to table
            if (!this.resultsAdded) {
            this.init_tableColumns.push(this.result_tableColumns)
            this.init_tableColumns= _.flattenDeep(this.init_tableColumns)
            }


            this.result_data.data[this.original_key] = _.merge({}, this.result_data.data[this.original_key], updated_results.data[this.original_key])
            this.result_data.csv_table = updated_results.csv_table
            this.result_data.zip_path = updated_results.zip_path

            this.upload_data_cp = this.upload_data

            this.upload_data[this.original_key] =  _.merge({}, this.upload_data_cp[this.original_key], this.result_data.data[this.original_key])

            this.upload_data[this.original_key]["measurements"] = this.result_data.data[this.original_key]["measurements"]


            this.warning1 = "Heads up! Change in the image with measurements might take time"
            this.changed[this.original_key] = false
            }

            else if (updated_results.status === "err") {

                this.error = results.message+"\n Something went wrong with the results update. Try again by clicking on 'x'. If the issue persists, contact us."
            }
    })
    },

    showPlot(data,unit) {
      // Set showPlotComponent to true to render the Plotly component
      this.showPlotComponent = true;
      // Set showModal to true to show the BootstrapVue modal
      this.showModal = true;
      this.data[0].x = data
      this.layout.xaxis.title += `(${unit})`
    },

    showInpImage(imagePath){
      this.imagePath = imagePath


      this.showModalInp=true
      fetch(pathCorrecter(imagePath))
        .then(response => response.arrayBuffer()) // Convert the response to an array buffer
        .then(arrayBuffer => {
          // Create a new Tiff object with the array buffer
          const tiff = new Tiff({ buffer: arrayBuffer });

          // Get the canvas containing the TIFF image
          const canvas = tiff.toCanvas();

          // Convert the canvas to a data URL
          const dataURL = canvas.toDataURL();

          // Set the data URL as the image source
          this.imageSrc = dataURL;
        })
        .catch(error => {
          console.error('Error loading TIFF image:', error);
        });

    },

    prepDraw(imagePath, original_file) {
      this.showModal = true;
      this.showPlotComponent = true;
      this.input_file = pathCorrecter(imagePath)
      this.original_key = original_file
      
    }, 

    showImage(imagePath){
        this.showPlotComponent=true
        this.showModal = true
        this.outimagePath= pathCorrecter(imagePath) 


    },

    clearPlot() {
      // Reset showPlotComponent when the modal is hidden
      this.showPlotComponent = false;
      this.showModal = false;
      this.layout.xaxis.title = "Measurements "
      this.$refs.myModal.hide()
    },

    exportCsv() {
        let blob = new Blob([this.result_data.csv_table], {type: 'text/csv;charset=utf-8' })
        const formatted_date = formatDate(new Date())
        saveAs(blob, `results_${formatted_date}.csv`)

    },

    exportImages() {
        const zipPath = this.result_data.zip_path
        this.loader_zip = true

        fetch(pathCorrecter(zipPath), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/zip'
        }
      })

      .then(response => {
        // Convert response to blob
        return response.blob();
      })
      .then(blob => {
        // Create object URL for the blob
        const url = window.URL.createObjectURL(blob);
        
        // Create a temporary anchor element
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        const formatted_date = formatDate(new Date())
        a.download = `measured_images_${formatted_date}.zip`; // Specify the file name
        
        // Append the anchor to the document body
        document.body.appendChild(a);
        
        // Trigger the click event on the anchor
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Error downloading zip file:', error);
      });

      this.loader_zip = false

      },

    example_image(inpFilePath) {
      // console.log("hi")

      fetch(`${API.baseURL}static/uploads/examples/`+inpFilePath)
      .then(response => {
          // Check if response is successful
          if (!response.ok) {
            throw new Error('Failed to fetch example image');
          }
          // Convert response to blob
          return response.blob();
      })
      .then(blob => {
          // Create object URL for the blob
          this.showExample = true;

          this.exampleImage = URL.createObjectURL(blob);
          this.user_hash = "examples"
          const file = new File([blob], inpFilePath, { type: 'image/tiff' });
          this.uploadedFiles = _.concat(this.uploadedFiles, file)
          this.uploadImages()

        })
        .catch(error => {
          console.error('Error fetching example image:', error);
        });
      },



    clear() {
      window.location.reload();
    },

    mounted(){
      this.lines[this.original_key].forEach(line => {
      line.length = this.calculateLineLength(line.start, line.end);
      });
      this.draw();
    },

},
  };
  </script>

  <style scoped>

  
  .table-container {
    max-height: 500px; /* Set the maximum height for the table */
    max-width: 100%;
    overflow-y: auto; /* Enable vertical scrolling if needed */
    padding-right: 10px;
    margin-top: 20px;
    padding:0px;
    border-width: 0px;
  }

  canvas {
  cursor: pointer;
  /* max-width: 200.0001%; 
  max-height: 101.0001%;  */

}

.modal-content{
  width:150%;
}

  .table-container th
  {
    padding: 10px 20px 10px 20px;
    text-align: center;
    position: relative;
}


.table-container td
  {
    padding: 10px 20px 10px 20px;
    text-align: center;
    position: relative;
}


  .drop-area {
    border: 2px dashed #605F5E;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    background-color: #ececec;
    margin: left;
    display: right;
    border-radius: 20px;
    flex: 1;
    width:100%;
  }

  .drop-area p {
    margin: 50px;
  }

  .drop-area.dragging {
    border-color: #4caf50;
  }

  .drop-area.disabled {
  background-color: #f2f2f2; /* Light gray background color */
  opacity: 0.5; /* Reduce opacity to visually indicate disabled state */
  pointer-events: none; /* Disable pointer events to prevent interaction */
}

  .progress-bar {
    height: 10px;
    background-color: #1F487E;
    padding:0;
    border-width: 0px;
  }

  .flash-enter-active /*.flash-leave-active*/ {
    transition: background-color .5s, box-shadow .5s, opacity .5s;
  }
  .flash-enter, .flash-leave-to {
      opacity: 0.5;
      background-color: #6f84ef;
      box-shadow: 0 0 0 16px #6f84ef;
  }

  .loading {
    opacity: 0.5; /* Adjust the opacity to make the table appear opaque */
    transition: opacity 0.5s;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
  }

  .spinner-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999; /* Ensure the spinner appears on top */
}

.btn-custom {
  color: lightgray; /* Gray text color */
  background-color: #fff; /* White background */
  border-color: lightgray; /* Gray border color */
}


.btn-load {
  border-color: #4caf50;
  background-color: white;
  color: #4caf50;
}

.btn-load-results {
  color: lightgray; /* Gray text color */
  background-color: #fff; /* White background */
  border-color: lightgray; /* Gray border color */
}

.btn-custom-results {
  color: #fff; /* White text color */
  background-color:  #4e9960; /* Green background color */
  border-color: #4e9960; /* Green border color */
}

.btn-custom-results:hover {
  color: #fff; /* White text color on hover */
  background-color: #218838; /* Darker green background on hover */
  border-color: #1e7e34; /* Darker green border color on hover */
}

.button-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
}

/* Adjust the width of buttons if needed */
.button-container .btn {
  width: 200px; /* Make buttons full width of container */
  margin-bottom: 5px; /* Add margin between buttons */
}


.axis path,
.axis line {
    fill: none;
    stroke: #000;
    shape-rendering: crispEdges;
}

.line {
    fill: none;
    stroke: lightgrey;
    stroke-width: 3px;
}

.img {
    width: 60%;
    height: 60%
}
.batch-results {
    width: 100%;
}

.custom-modal {
  /* Example styles, modify as needed */
  background-color: #f0f0f0;
  border: 2px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 150%;
  margin: 0 auto;
  padding: 20px;
  color: #333;

}

.child-modal .modal-content{
  width: 150%;
}

/* Custom styling for modal content container */
.modal-content{
  display: flex;
  align-items: center;      
  justify-content: center;  
  height: 100%;             
  width: 150%;
}

div.tooltip-plot {
    position: absolute;
    text-align: left;
    padding: .5rem;
    background: #FFFFFF;
    color: #313639;
    border: 1px solid #313639;
    border-radius: 8px;
    pointer-events: none;
    font-size: 12px;
}

.editable {
  color: green;
}

.not-editable {
  color: lightgray;
}


  </style>
