# import the necessary packages
#from skimage.measure import structural_similarity as ssim
#from skimage import measure
from skimage.metrics import structural_similarity
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import pysift
import json


def mse(imageA, imageB):
    	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
 
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title, isImgOn):
    # compute the mean squared error and structural similarity

    MSE = mse(imageA, imageB)
    SSIM = structural_similarity(imageA, imageB)
    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (MSE, SSIM ))
    #plt.suptitle("SSIM: %.2f" % (s))
    
    
    #### for check images, not needed
    if isImgOn == True:
    
        # show first image
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(imageA, cmap = plt.cm.gray)
        plt.axis("off")
        # show the second image
        ax = fig.add_subplot(1, 2, 2)
        plt.imshow(imageB, cmap = plt.cm.gray)
        plt.axis("off")
        # show the images
        plt.show()
    
    return MSE, SSIM

 
 
def image_resize(path_1, path_2, new_size):
    image_1 = Image.open(path_1)
    new_image_1 = image_1.resize((new_size, new_size))
    new_image_1.save("input_1_"+str(new_size)+".jpg")
    
    image_2 = Image.open(path_2)
    new_image_2 = image_2.resize((new_size, new_size))
    new_image_2.save("input_2_"+str(new_size)+".jpg")   
    
    
    
if __name__ == "__main__":
     
    # load the images -- the original, the original + contrast,
    # and the original + photoshop
    
    new_size = 512
    input_1 = "image_samples/JangiriPonpon_003.jpg"
    input_2 = "image_samples/west_012.jpg"
    
    
    #### resize to same dimention
    image_resize(input_1, input_2, new_size)
    
    
    saved_input_1 = "input_1_"+str(new_size)+".jpg"
    saved_input_2 = "input_2_"+str(new_size)+".jpg"
    
    original = cv2.imread(saved_input_1, cv2.IMREAD_COLOR)
    contrast = cv2.imread(saved_input_2, cv2.IMREAD_COLOR)
    
    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    
    
    
    ##### sift
    limit_sift = 1000
    sift = cv2.xfeatures2d.SIFT_create(limit_sift)
    
    
    keypoints_sift_1, descriptors_1 = sift.detectAndCompute(original, None)
    keypoints_sift_2, descriptors_2 = sift.detectAndCompute(contrast, None)
    
    #### for debug
    #print(descriptors_1.shape)
    np.set_printoptions(threshold=sys.maxsize)    
    

    DIST = np.linalg.norm(descriptors_1-descriptors_2)
    print(DIST)
    

    
    # initialize the figure
    fig = plt.figure("Images")
    images = ("Original", original), ("Contrast", contrast)
    # # loop over the images
    # for (i, (name, image)) in enumerate(images):
    #     # show the image
    #     ax = fig.add_subplot(1, 2, i + 1)
    #     ax.set_title(name)
    #     plt.imshow(image, cmap = plt.cm.gray)
    #     plt.axis("off")
    # show the figure
    #plt.show()
    # compare the images
    MSE, SSIM = compare_images(original, contrast, "Original vs. Contrast", False)
    
    similarity = MSE+SSIM+DIST
    print("SIMILARITY = "+str(similarity))
