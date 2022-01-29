# deforestation
Identification of déforestation in primary forest zones using SAR images from the Copernicus program
The following steps helps you analyse SAR images of satelites. You first need to select the zone of interest in the world. Then downloaded several images (on PEPS website of Copernicus Scihub) of the zone an proced to a standarisation of the said pictures (calibiration and normalisation) on the SNAP software. 
Once, it is done, you can proced with the folowing steps. 


# STEP 0 : import the necessary packages. (see the code)

# STEP 1 : transform images into matrix containing the intensity of each pixels so we can analayse their evolution.

# STEP 2 : extract the images with the following code and print it to see the shape in your terminal.
We took an example with 5 images of the same zone. Its important that theses images are correctly calibrated so that each pixel correspond to the same place for each image.
It's also important to choose VH or HV for the polarisation of the image. If you want to know why, a quick explanation is available in the README.md

# STEP 3 : create a criteria to explicit the evolution of the forest between two images. You can apply the following code to the 5 images above.
the criteria. (you can find the right threshold with the code in the Appendix with the code in step 4)

# STEP 4 : Caluculate the mean evolution of the intensity.
please notice that we are still taking our set of 5 Radar pictures.
One can adapt the code to x pictures.
Code pour faire apparaître l'évolution de l'intensité des pixels.
as we said before, each picture must be calibrated on the first one. So they have the same size.
we will compute the evolution for each pixel, but we can't represent the evolution of each one.
So we chose to display the geastest evolution of intensity (bestscore), the lowest (baddestscore) and the mean evoltion on the entire picture.
Before getting on with the rest of the steps, please compare your results with mine.

If your results are close to the classical evolution of pixels on deforestation as displayed in the Appendix, you can procede with the next step to identified the precise location of the deforestation.
Else, please skip the next step.

# STEP 5 : Here is the code to apply step 4 localy.
let's take an example of a deforestated zone on the SAR (corresponding to the following pixels) :
You can find the right zone using the following code :

# STEP 6 : let's progressively overlay (with colors) these changes to explicit the deforestated zone.
then paste the new colored image on the precedent.
you can use as a initial background, the images obtained in the STEP 3.
if this method doesn't work, you can use the precedent code to create progressively colored pictures (coressponding to the changes), using the following code
