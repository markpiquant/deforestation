# STEP 0 : import the necessary packages.

from glob import glob
from pyparsing import quotedString
from spectral import open_image
from numpy import reshape
from math import *
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from random import *

# STEP 1 : transform images into matrix containing the intensity of each pixels so we can analayse their evolution.
# In step X, we will see how this evolution helps us caracterize a potential modification in the forest.


def extractImg(zipPath, zipName, imageName):
    """
    entrées :
    zipPath: file with .dim documents
    zipName: name of one .dim document
    imageName: name of band polarisation located in the .dim file (for instance : Sigma0_VH or Sigma0_VV)

    sortie : 
    matrix containing the intensité of each pixel
    """

    zipName = zipName[:-4] + '.data'
    fileName = glob(zipPath + "\\" + zipName + "\\" + imageName + ".hdr")
    return open_image(fileName[0]).open_memmap(writeable=True)

# STEP 2 : extract the images with the following code and print it to see the shape in your terminal.


A = extractImg("file of your working directory where you downloaded the images",
               "subset_1_of_03312021.dim", "Sigma0_VH")
B = extractImg("file of your working directory where you downloaded the images",
               "subset_3_of_03072021.dim", "Sigma0_VH")
C = extractImg("file of your working directory where you downloaded the images",
               "subset_4_of_02232021.dim", "Sigma0_VH")
D = extractImg("file of your working directory where you downloaded the images",
               "subset_5_of_04122021.dim", "Sigma0_VH")
E = extractImg("file of your working directory where you downloaded the images",
               "subset_6_of_03192021.dim", "Sigma0_VH")

# We took an example with 5 images of the same zone. Its important that theses images are correctly calibrated so that each pixel correspond to the same place for each image.
# It's also important to choose VH or HV for the polarisation of the image. If you want to know why, a quick explanation is available in the README.md

# STEP 3 : create a criteria to explicit the evolution of the forest between two images. You can apply the following code to the 5 images above.
# the criteria. (you can find the right threshold with the code in the Appendix with the code in step 4)
x = 0.03
F = abs(D-E)  # take two matrix corresponding to two periods
K = F > x  # apply the criteria to show only the pixel where the a singificant evolution is seen
I = np.array(K)
np_img_2 = np.squeeze(I, axis=2,)  # axis=2 is channel dimension
im_2 = Image.fromarray(np_img_2)
im_2.save('comparison_btw.png')

# STEP 4 : Caluculate the mean evolution of the intensity.
# please notice that we are still taking our set of 5 Radar pictures.
# One can adapt the code to x pictures.
# Code pour faire apparaître l'évolution de l'intensité des pixels.


A_pr = np.squeeze(A, axis=2,)  # create a matrix the size of the image.
B_pr = np.squeeze(B, axis=2,)
C_pr = np.squeeze(C, axis=2,)
D_pr = np.squeeze(D, axis=2,)
E_pr = np.squeeze(E, axis=2,)


# as we said before, each picture must be calibrated on the first one. So they have the same size.
a = len(A_pr)
b = len(A_pr[0])

# we will compute the evolution for each pixel, but we can't represent the evolution of each one.
# So we chose to display the geastest evolution of intensity (bestscore), the lowest (baddestscore) and the mean evoltion on the entire picture.
# the date of the SAR images in abscissa
x = ["23_fev", "7_mars", "19_mars", "31_mars", "12_avril"]
bestscore = [A_pr[1][1], B_pr[1][1], C_pr[1][1], D_pr[1][1], E_pr[1][1]]
baddestscore = [A_pr[1][1], B_pr[1][1], C_pr[1][1], D_pr[1][1], E_pr[1][1]]
meanscore = [0, 0, 0, 0, 0]
n = 0
for i in range(1, a):
    for j in range(1, b):
        a = A_pr[i][j]
        b = B_pr[i][j]
        c = C_pr[i][j]
        d = D_pr[i][j]
        e = E_pr[i][j]
        Y = [a, b, c, d, e]
        n += 1
        for k in range(0, 5):
            meanscore[k] = meanscore[k]+Y[k]
        if abs(Y[1]-Y[0]) > abs(bestscore[1]-bestscore[0]):
            bestscore = Y
        if abs(Y[1]-Y[0]) < abs(baddestscore[1]-baddestscore[0]):
            baddestscore = Y
for k in range(0, 5):
    meanscore[k] = meanscore[k]/n
print(bestscore)
print(meanscore)
print(baddestscore)
plt.plot(x, meanscore, label="""évolution moyenne d'un pixel""")
plt.plot(x, bestscore, label="""évolution maximale d'un pixel""")
plt.plot(x, baddestscore, label="""évolution minimale d'un pixel""")
plt.title("""Evolution de l'intensité des pixels dans l'image""")
plt.grid(True)
plt.legend()
plt.show()

# Often, the difference between bestscore and baddestscore isn't very obvious graphically.
# You can type this in order to have a better understanding of the intensity repartition.
#           print(bestscore)
#           print(meanscore)
#           print(baddestscore)

# Before getting on with the rest of the steps, please compare your results with mine.
# If your results are close to the classical evolution of pixels on deforestation as displayed in the Appendix, you can procede with the next step to identified the precise location of the deforestation.
# Else, please skip the next step.

# STEP 5 : Here is the code to apply step 4 localy.

# let's take an example of a deforestated zone on the SAR (corresponding to the following pixels) :
#left = 2100
#top = 2000
#width = 900
# height = 500


# You can find the right zone using the following code :
im = Image.open("analyse/subset_1_of_03312021.data/Sigma0VH")
left = 2100
top = 2000
width = 900
height = 500
box = (left, top, left+width, top+height)
# Crop Image
area = im.crop(box)
area.save('forêt_primaire.png')


def deforestated_zones(A):
    x = 500
    y = 900
    A_sec = np.zeros((x, y))
    for i in range(0, 500):  # ligne 2000 à 2500 colonnes 2100 à 3000
        for j in range(0, 900):
            A_sec[i][j] = A[i+2000][j+2100]
    return A_sec


A_br = deforestated_zones(A=np.squeeze(
    np.array(extractImg("analyse/", "subset_4_of_02232021.dim", "Sigma0_VH"))))
B_br = deforestated_zones(A=np.squeeze(
    np.array(extractImg("analyse/", "subset_3_of_03072021.dim", "Sigma0_VH"))))
C_br = deforestated_zones(A=np.squeeze(
    np.array(extractImg("analyse/", "subset_6_of_03192021.dim", "Sigma0_VH"))))
D_br = deforestated_zones(A=np.squeeze(
    np.array(extractImg("analyse", "subset_1_of_03312021.dim", "Sigma0_VH"))))
E_br = deforestated_zones(A=np.squeeze(
    np.array(extractImg("analyse/", "subset_5_of_04122021.dim", "Sigma0_VH"))))


# récupère l'évolution de l'intensité pour les zones brûlées.
b = len(A_br)
x = ["23_fev", "7_mars", "19_mars", "31_mars", "12_avril"]
bestscore = [A_br[1][1], B_br[1][1], C_br[1][1], D_br[1][1], E_br[1][1]]
baddestscore = [A_br[1][1], B_br[1][1], C_br[1][1], D_br[1][1], E_br[1][1]]
meanscore = [0, 0, 0, 0, 0]
n = 0
for i in range(1, b):
    c = len(A_br[i])
    for j in range(1, c):
        a = A_br[i][j]
        b = B_br[i][j]
        c = C_br[i][j]
        d = D_br[i][j]
        e = E_br[i][j]
        Y = [a, b, c, d, e]
        n += 1
        for k in range(0, 5):
            meanscore[k] = meanscore[k]+Y[k]
        if abs(Y[1]-Y[0]) > abs(bestscore[1]-bestscore[0]):
            bestscore = Y
        if abs(Y[1]-Y[0]) < abs(baddestscore[1]-baddestscore[0]):
            baddestscore = Y
for k in range(0, 5):
    meanscore[k] = meanscore[k]/n
print(bestscore)
print(meanscore)
print(baddestscore)
plt.plot(x, meanscore, label="""évolution moyenne d'un pixel""")
plt.plot(x, bestscore, label="""évolution maximale d'un pixel""")
plt.plot(x, baddestscore, label="""évolution minimale d'un pixel""")
plt.title("""Evolution de l'intensité des pixels dans l'image""")
plt.grid(True)
plt.legend()
plt.show()


# STEP 6 : let's progressively overlay (with colors) these changes to explicit the deforestated zone.

x = 0.03  # our previous threshold
F = abs(D-E)  # take two pricture in temporal order
K = F > x

# a and b are the size of ecah matrix
img = Image.new("RGB", (a, b), (255, 255, 255))
for x in range(1, a):
    for y in range(1, b):
        if K[x][y] == True:
            b = 255  # you can change the color of the pixel here
            v = 0
            r = 0
        else:
            b = 0
            v = 0
            r = 0

        img.putpixel((x, y), (r, v, b))
img.save("color D_E.png")

# then paste the new colored image on the precedent.
# you can use as a initial background, the images obtained in the STEP 3.
background = Image.open("color.png").convert("RGBA")
img = Image.open("color_D_E.png")
x, y = img.size
background.paste(img, (x, y), img)
background.paste(background, (x, y), background)
background.save('color_A_B.png', format="png")

# if this method doesn't work, you can use the precedent code to create progressively colored pictures (coressponding to the cahnges), using the following code
img = Image.open("Color A_B_C_D.png")
for x in range(1, 5001):
    for y in range(1, 5101):
        if K[x][y] == True:
            b = 0
            v = 255
            r = 255
        else:
            b = 0
            v = 0
            r = 0

        img.putpixel((x, y), (r, v, b))
img.save("color A_B_C_D_E.png")


# Appendix : Code to find the right treshold in the 3rd step :
F = abs(C-E)
for i in range(1, 100):
    # the pixel appears in white on the image if the intensity of the spread between the two image is enough
    B = F > 0.001 + i*0.001
    H = np.array(B)
    np_img_i = np.squeeze(H, axis=2,)  # axis=2 is channel dimension
    im_i = Image.fromarray(np_img_i)
    im_i.save('comparaison fev_mars_i.png')
