#!/usr/bin/python3
# CODE for checking a specific folder and running the diameter measuring pipeline #
# libraries
import cv2
import numpy as np
import time
import re
import pandas as pd
import inspect

## helper functions ##
from fibar_module.classical_segmenter import classical_segment
from fibar_module.scale_obtain import scale_obtain
from fibar_module.thinner import thinner, thinner_2k_5k
from fibar_module.point_picker import point_picker
from fibar_module.dm_finder import dm_finder

def scaling(PATH_1: str):
    return scale_obtain(PATH_1)

def drawer(PATH_1:str, coords:list, caller_id:int):

    rgb_im = cv2.imread(PATH_1)

    start_color = (0, 0, 0)
    end_color = (255,0,0)
    start_end_coords = []


    if caller_id == 1:

        for combo in coords:

            start_point = [combo[1], combo[0]]
            mid_point = [combo[3], combo[2]]

            # testing the actual end point
            end_point_x = (2 * mid_point[0]) - start_point[0]
            end_point_y = (2 * mid_point[1]) - start_point[1]

            end_point = [end_point_x, end_point_y]

            start_end_coords.append([start_point, end_point])


            distance1 = np.sqrt((end_point[1] - start_point[1]) ** 2 + (end_point[0] - start_point[0]) ** 2)

            cv2.line(rgb_im, start_point, end_point, start_color, 2)

            cv2.circle(rgb_im, start_point, 2, end_color, -1)
            cv2.circle(rgb_im, end_point, 2, end_color, -1)

        image = cv2.cvtColor(rgb_im, cv2.COLOR_RGB2BGR)

    else:
        for combo in coords:
            combo = sum(combo, [])
            start_point = [combo[0], combo[1]]
            end_point =  [combo[2], combo[3]]
            start_end_coords.append([start_point, end_point])
            cv2.line(rgb_im, start_point, end_point, start_color, 2)

            cv2.circle(rgb_im, start_point, 2, end_color, -1)
            cv2.circle(rgb_im, end_point, 2, end_color, -1)

        image = cv2.cvtColor(rgb_im, cv2.COLOR_RGB2BGR)



    return np.uint8(image), start_end_coords


def measure_dm(PATH_1:str, points:int, scales: None, cmd_line_based:bool):

    start_time = time.time()

    ## CLASSICAL segmentation ##
    # otsu thresholding for 2k and 5k and 500x if specified in path
    if PATH_1.endswith("png") or PATH_1.endswith("jpg") or PATH_1.endswith("tif"):

        # distance values in pixels
        dist_bool = False

        if re.search("(5k|2k|500x|500k)", PATH_1) != None: # if there is no mag in the file name

            segmented_im = cv2.threshold(cv2.imread(PATH_1, 0), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
            dist, thinned = thinner_2k_5k(segmented_im)

        else:
            # classical segmentation for other magnifications
            segmented_im = classical_segment(PATH_1)

            dist, thinned = thinner(segmented_im)

        # 100 measurements per image
        pt_s = point_picker(segmented_im, points)

        # prints out diameters
        #print(f"Measured diameters in nm {first_dm_s}" if dist_bool== False else f"Measured diameters in px {first_dm_s}")
        #print("It took", time.time() - start_time, "seconds, to analyse the image")


        ## DIAMETERS VISUALIZATION ##

        if cmd_line_based and scales is None:

            scales = scale_obtain(PATH_1)
        #print(scales)
            try:
                if len(scales) == 3:
                    if scales[1] == "um":
                        nano_per_px = int(scales[0]) * 1000 / int(scales[-1])
                # scale = nm
                    elif scales[1] == "nm":
                        nano_per_px = int(scales[0]) / int(scales[-1])

                    else:
                        dist_bool = True
                        nano_per_px = 1
                

            except:
                # adding a file for scale exception
                nano_per_px = 1
                dist_bool = True

            # leaving the lower part (scale included) in for now
            h,w = segmented_im.shape[:2]

            first_dm_s, first_excs, coords  = dm_finder(thinned, dist, segmented_im, pt_s, h,w,nano_per_px)

            print(f"Measured diameters in nm {first_dm_s}" if not dist_bool else f"Measured diameters in px {first_dm_s}")
            print("It took", time.time() - start_time, "seconds, to analyse the image")

            image, start_end_coords = drawer(PATH_1, coords, 1)

        else: # not cmd line based
   
            try:

                if scales[1] == "um":
                    nano_per_px = int(scales[0]) * 1000 / int(scales[-1])
            # scale = nm
                elif scales[1] == "nm":
                    nano_per_px = int(scales[0]) / int(scales[-1])

                else:
                    dist_bool = True
                    nano_per_px = 1

            except:
                # adding a file for scale exception
                nano_per_px = 1
                dist_bool = True

            # leaving the lower part (scale included) in for now
            h,w = segmented_im.shape[:2]

            first_dm_s, first_excs, coords  = dm_finder(thinned, dist, segmented_im, pt_s, h,w,nano_per_px)

            image, start_end_coords = drawer(PATH_1, coords, 1)

            return [dist_bool, first_dm_s, np.uint8(image), start_end_coords]            
