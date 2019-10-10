# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import nlp_spaCy

# Adding tesseract into our path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Auxiliary
def load_img(path_to_img):
    # Apply OCR
    # load the example image and convert it to grayscale
    image = cv2.imread(path_to_img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray

def preprocess_img(preprocess_type, gray):
    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess_type == "thresh":
        gray_preprocessed = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess_type == "blur":
        gray_preprocessed = cv2.medianBlur(gray, 3)
    
    return gray_preprocessed

def apply_OCR(gray_preprocessed):
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray_preprocessed)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print(text)
    return text

def display_imgs(image, gray_preprocessed, _display):
    if _display == "True":
        # show the output images
        cv2.imshow("Image", image)
        cv2.imshow("Output", gray_preprocessed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

def main():
    print("========================== Loading Main method ==========================")
     # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
        help="type of preprocessing to be done")
    ap.add_argument("-d", "--displayIMGs", type=str, required=True, 
        help="user could choose to display images(original image and preprocessed image)")
    args = vars(ap.parse_args()) 
    
    image, gray = load_img(args["image"])
    gray_preprocessed = preprocess_img(args.get("preprocess"), gray)
    text_extracted = apply_OCR(gray_preprocessed)
    display_imgs(image, gray_preprocessed, args["displayIMGs"])

if __name__ == "__main__":
    main()