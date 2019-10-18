# import the necessary packages
from wand.image import Image as wi
from wand.display import display as wd
from wand.color import Color as wc
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from nlp_analysis import findDates

# Adding tesseract into our path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Default file path to the output images converted from pdfs
CONVERTED_PDF_IMAGE_DIR = ".\\pdfs\\converted_pdf_images"

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
    output_dir = os.path.join(output_path, os.path.splitext(os.path.basename(filename))[0])
    
    # Check if an output directory exists, if not then create one. Else continue
    if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)
    
    image_file_dir = os.path.join(output_dir, "image_files")
    # Check if the sub directory (image_files) exists, if not then create one. Else continue
    if os.path.isdir(image_file_dir) == False:
        os.mkdir(image_file_dir)
    
    for i, page in enumerate(all_pages.sequence):
        with wi(page) as img:
            img.format = 'png'
            img.background_color = wc('white')
            img.alpha_channel = 'remove'

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = '{}_{}.png'.format(image_filename, i)
            image_filename = os.path.join(image_file_dir, image_filename)
            
            img.save(filename=image_filename)

def save2Txt(filename, page_num, extracted_text, output_path):
    output_dir = os.path.join(output_path, os.path.splitext(os.path.basename(filename))[0])
    text_file_dir = os.path.join(output_dir, "text_files")
    
    # Check if the sub directory (text_files) exists, if not then create one. Else continue
    if os.path.isdir(text_file_dir) == False:
        os.mkdir(text_file_dir)
    
    text_filename = os.path.splitext(os.path.basename(filename))[0]
    text_filename = "{}_{}.txt".format(text_filename, page_num)
    textFile_path = os.path.join(text_file_dir, text_filename)
    
    with open(textFile_path, 'a+') as txtFile:
        txtFile.write(extracted_text)

def sort_image_list(images_list):    
    # Sort the list of images by page 
    sorted_list = sorted(images_list, key=lambda n : int((n.split('_')[1][:-4])))
    return sorted_list

'''
Main function
'''        
def main():
    print("========================== Loading Main method ==========================")
    # Call the parseArgs function to parse user's command line arguments
    args = parseArgs()
    
    # If a pdf file path is given, then we need to use "wand" to convert the pdf into image first 
    if args["pdf"]:
        path_to_pdf = args["pdf"]
        convert_pdf(path_to_pdf, CONVERTED_PDF_IMAGE_DIR)  # A list of images converted from the input pdf 
    
    images_path = os.path.join(CONVERTED_PDF_IMAGE_DIR, os.path.splitext(os.path.basename(args["pdf"]))[0])   
    images_path = os.path.join(images_path, "image_files")        
    images_list = os.listdir(images_path)
    images_list_sorted = sort_image_list(images_list)
    
    for page_num, img_name in enumerate(images_list_sorted):
        print(f"++++++++++++++++++++++++ page {page_num} ++++++++++++++++++++++++")
        
        img_path = os.path.join(images_path, img_name)
        # Load and read image using cv2
        image, gray = load_img(img_path)
        
        # Preprocess the gray image we obtained earlier
        gray_preprocessed = preprocess_img(args.get("preprocess"), gray)
        
        # Store the text extracted from the image
        text_extracted = apply_OCR(gray_preprocessed)
        print(text_extracted)
        
        # Save extracted page content into its corresponding .txt file
        save2Txt(args['pdf'], page_num, text_extracted, CONVERTED_PDF_IMAGE_DIR)
        
        print("++++++++++++++++++++++++ End of page ++++++++++++++++++++++++")
        print('')
        
        # **Optional** Display original image and preprocessed image
        display_imgs(image, gray_preprocessed, args["displayIMGs"])
    
if __name__ == "__main__":
    main()