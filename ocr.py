# import the necessary packages
from wand.image import Image as wi
from wand.display import display as wd
from wand.color import Color as wc
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import nlp_analysis as na

# Adding tesseract into our path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Auxiliary
def parseArgs():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default="",
        help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
        help="type of preprocessing to be done")
    ap.add_argument("-d", "--displayIMGs", type=str, default="False", 
        help="user could choose to display images(original image and preprocessed image)")
    ap.add_argument("-pdf", "--pdf", type=str, default="", 
        help="path to input pdf to be OCR'd")
    args = vars(ap.parse_args()) 
    return args

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
   
def convert_pdf(filename, output_path, resolution=300):
    """ Convert a PDF into images.

        All the pages will give a single png file with format:
        {pdf_filename}-{page_number}.png

        The function removes the alpha channel from the image and
        replace it with a white background.
    """
    all_pages = wi(filename=filename, resolution=resolution)
    for i, page in enumerate(all_pages.sequence):
        with wi(page) as img:
            img.format = 'png'
            img.background_color = wc('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}-{}.png'.format(image_filename, i)
            image_filename = os.path.join(output_path, image_filename)

            img.save(filename=image_filename)

'''
Main function
'''        
def main():
    print("========================== Loading Main method ==========================")
    # Call the parseArgs function to parse user's command line arguments
    args = parseArgs()
    images = []
    
    # If a pdf file path is given, then we need to use "wand" to convert the pdf into image first 
    if args["pdf"]:
        path_to_pdf = args["pdf"]
        convert_pdf(path_to_pdf, ".\\pdfs\\converted_pdf_images")  # A list of images converted from the input pdf 
        
    if args["image"] or (len(images) != 0):
        # Load and read image using cv2
        image, gray = load_img(args["image"])
        
        # Preprocess the gray image we obtained earlier
        gray_preprocessed = preprocess_img(args.get("preprocess"), gray)
        
        # Store the text extracted from the image
        text_extracted = apply_OCR(gray_preprocessed)
        
        # **Optional** Display original image and preprocessed image
        display_imgs(image, gray_preprocessed, args["displayIMGs"])
    
    else:
        print("There is no image file path given.")
    
if __name__ == "__main__":
    main()