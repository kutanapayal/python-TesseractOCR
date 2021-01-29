# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2 as cv
import os
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

image = cv.imread(args["image"])
cv.imshow('image',image)
gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray = cv.threshold(gray,0,255, cv.THRESH_BINARY|cv.THRESH_OTSU)[1]
elif args["preprocess"] == "blur":
    gray = cv.medianBlur(gray,3)

filename = "{}.jpg".format(os.getpid())
cv.imshow('Gray',gray)
cv.imwrite(filename,gray)
filename=os.getcwd() +"/"+ filename
print(filename)
# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
text = pytesseract.image_to_string(filename)
os.remove(filename)
print(text)

cv.waitKey(0)

# Run it as -->
# python fatch_character.py --image C:\Users\LENOVO\Desktop\Bacancy\python_opencv\picture\cat.jpg --preprocess "thresh"