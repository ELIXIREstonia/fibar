import fibar

# enter absolute filepath here
IMG_FILE_PATH = "examples/sem/10k_example.tif" 

# nr of diameters measurements expected 
nr_of_measurements = 10 

# if you want an image where the diameters are located (estimate)
img_with_the_estimated_lines = True 

fibar.measure_dm(IMG_FILE_PATH, nr_of_measurements, True)
