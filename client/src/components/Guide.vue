<template>
  <div class="container">

    <div class="col-md-9">
      <h4>FiBar: diameter measuring tool</h4>
      <p>
        Measuring fiber diameters from scanning electron microscopy (SEM) images automatically. 
      </p>
      <br>

      <h5> Overview </h5>
      <p>
        Given an SEM image of TIF/JPG/PNG format and the amount of measurement points, the tool provides a diameters' analysis of the fibrous sample. The analysis includes standard metrics, such as mean, median, standard deviation as well as a histogram of the measurements and image with the measured points.
        <br>FiBar has been created in collaboration with the Institute of Pharmacy, as the need for an alternative to manual measurements became more pressing. The tool employs classical image processing methods (such as distance transform, thinning, Kuwahara filtering etc.) as well as neural networks (PyTesseract, ResNet). 
      </p>
      <br>
      <h5> Requirements </h5>
      <p>
        In order for the tool to work as intended, the following is expected from the input files: 
        <ul>
        <li> <b> Format: </b>the input file is either TIF(F), JPG, PNG;</li>
        <li> <b> File name: </b> 
          <ul>
            <li>
            for the best possible segmentation, the file name should include the magnification (especially for smaller magnifications), some examples: "example_2k.tif" or "this_is_a_sem_5k.png";
           </li>
           <li>
            all of the file names should be unique; 
           </li>
          </ul>
        </li>
        <li>
           <b> Content: </b> 
           <ul>
           <li>the input file should be the original SEM image; </li>
           <li>for automatic pixel-to-unit conversion, the scalebar expected to be on the bottom left of the image and the numeric value should be in white on a black background, as so: <img src="../assets/diff_scales.png" alt="Different scales" class="scale-image"> </li>
           <li>in case the digit/unit recognition is faulty, the user can correct the prediction by clicking on the according cell, the original image can also be found when clicked on the file name in the table; </li>
           <li>if the scale bar is not detected at all, the program will provide measurements in pixels;</li>
           </ul>
      </li>
        </ul>
      </p>
      <h5> How to use the tool?</h5>
      <p>
        <ol>
          <li> The user uploads image(s), by dragging images to the drop-area or by clicking on the drop area. If the user does not have any images, they simply can upload an example image.</li>
          <li> Once the correct files have been added, click "Upload"; </li>
          <li> During the uploading, the image will also be scanned for the scale. If the scalebar is found with the digit and unit, the output table will show the digit and unit accordingly. If there are some faulties in the digit/unit, the user can edit these by clicking on the according cell (the image is linked in the file name). In case the scale bar is not in the correct location or is missing, the system will provide the measurements in pixels.</li>
          <li> Once you have ensured that the scale is correct, enter the number of measurements (possible to provide values from 1 to 1000) expected from the image. Then click "Analyze".</li>
          <li> Depending on the amount of measurements, images and the image magnification, it will take some time (60-90s per 100 measurements per image). Please do not close the window/refresh the page as this will require to restart the process again.</li>
          <li> The results table will provide an overview of the results: mean, median and standard deviation and other meta. When you click on "Show results", you will see the histogram of measurements (the plot is exportable in the same window) as well as the image with measurements. If you want to do some analysis of your own, you can export the data by clicking on "Export CSV", it is also possible to export the images with measurements. In case of having more than one image, the exported CSV will include a row of data for each image.</li>
        </ol>
      </p>
      <h5>Disclaimer</h5>
      <p> Please use this tool responsibly, it might not always provide the most accurate measurements, so do check the image with measurements for clarity. By no means is this tool 100% accurate, the segmentation of fibers may be faulty depending on the image. Fortunately, a better apporach is in development - stay tuned! For tracking the developments, the project repo can be found <a href="https://gitlab.cs.ut.ee/elixir/fibar">here.</a></p>
      <h5>Questions?</h5>
      <p> In the likelihood of any questions, please contact us <a href="mailto:elixir.support@ut.ee?subject=FiBar%20support%20request"> by clicking here.</a></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserGuide',
}
</script>

<style scoped>
section {
  margin-bottom: 20px;
}
h6 {
  font-weight: bold;
  color: #333;
}
p {
  margin-left: 20px;
}
</style>
