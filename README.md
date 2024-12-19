# FiBar: diameter measuring tool

## Project Objective
The goal of this project is to provide an automated microscopy image analysis tool for complex biomaterials. These are samples of electrospun fibers with encapsulated components, such as bacteria, drugs etc. The ultimate goal of this tool is to reduce the workload of the researcher by providing a viable alternative to the manual analysis.

## "FiBar" webtool
The fiber diameter measuring web tool is accessible to all [https://fibar.elixir.ut.ee/](https://fibar.elixir.ut.ee/)

## How to install and run the Python module
The pipelines should be executed in the Python 3.8.10 environment (have not tested out other versions yet). All of the required libraries and their versions can
be installed from the <code>requirements.txt</code> file or running `pip install -e .`.

```
git clone git@github.com:ELIXIREstonia/fibar.git
cd fibar/scripts
pip install -r requirements.txt || pip install -e . 
```

NB! for obtaining diameter in nanometers, please make sure the Tesseract-OCR has been installed to your system and the `tesseract.exe` path has been added to `fibar_module/scale_obtain.py` in the commented location. A Stack Overflow post about the setup is provided [here](https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i)

The `examples` folder includes subfolder with microscopy data (`sem`) for testing out the package.

```
import fibar

# enter absolute filepath here
IMG_FILE_PATH = "examples/sem/10k_example.tif" 

# nr of diameters measurements expected 
nr_of_measurements = 10 

# if you want an image where the diameters are located (estimate)
img_with_the_estimated_lines = True 

fibar.measure_dm(IMG_FILE_PATH, nr_of_measurements, True)
```

## Constraints of "Fibar"

For the fiber analysis pipeline, the system assumes the following:
- the SEM input image can be TIF/PNG/JPG format;
- the file name should include a reference to the magnification used - "_2k_" or "_5k_" if a magnification of 2k (2000x) or 5k (5000x) was used;
- the OCR part of the pipeline assumes that the value and unit are provided in white
highlighted in black and the horizontal bar is white on a transparent background
aligned below the value and unit (nm or um).
