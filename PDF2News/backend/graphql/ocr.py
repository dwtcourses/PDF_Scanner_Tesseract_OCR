# import the necessary packages
from wand.image import Image as wi
from wand.display import display as wd
from wand.color import Color as wc
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import shutil
import numpy as np

# Adding tesseract into our path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Default PDFs directory
PDF_DIR = ".\\PDF2News\\backend\\pdfs"

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

def erode_img(gray, kernel_size=(1,1)):
    ''' Erosion - A type of Morphological Transformation
    
        erode_img(gray): The basic idea of erosion is just like soil erosion only, 
        it erodes away the boundaries of foreground object (Always try to keep foreground in white).
        
        The kernel slides through the image (as in 2D convolution). 
        A pixel in the original image (either 1 or 0) will be considered 1 only if all the pixels under the kernel is 1, 
        otherwise it is eroded (made to zero).
        
        Finally, all the pixels near boundary will be discarded depending upon the size of kernel. 
        So the thickness or size of the foreground object decreases or simply white region decreases in the image. 
        It is useful for removing small white noises, detach two connected objects etc.
    '''
    kernel = np.ones(kernel_size, np.uint8) 
    erosion = cv2.erode(gray, kernel, iterations=1)
    return erosion
    
def dilate_img(gray, kernel_size=(1,1)):
    ''' Dilation - A type of Morphological Transformation

        dilate_img(gray): It is just the opposite of erosion. 
        Here, a pixel element is ‘1’ if atleast one pixel under the kernel is ‘1’.
        So it increases the white region in the image or size of foreground object increases.
         
        Normally, in cases like noise removal, erosion is followed by dilation. 
        Because, erosion removes white noises, but it also shrinks our object. 
        So we dilate it. Since noise is gone, they won’t come back, but our object area increases. 
        It is also useful in joining broken parts of an object.
    '''
    kernel = np.ones(kernel_size, np.uint8) 
    dilation = cv2.dilate(gray, kernel, iterations=2)
    return dilation

def preprocess_img(filename, output_path, page_num, preprocess_type, gray):
    ''' A function to preprocess images converted from a PDF
    
        Args: 
            filename: The filename of the image to be preprocessed. (eg. 190916-VARSWAP-BARCLAYS-582619_1.png) 
            output_path: The output directory where we would like to store the preprocessed image in.
            page_num: The corresponding page number of the image that refers to the original PDF.
            preprocess_type: By default it's set to Otsu's Threshold.
            gray: The actual image (grayscaled) object we want to preprocess. The image is stored as numpy.array.
            
        Returns:
            preprocessed_img: The preprocessed image object, and it can be passed to the next step, which is to apply OCR on it and extract text/content from it.
    '''
    # Perform morphological transformations 
    gray_preprocessed = dilate_img(gray)   # Dilate the grayscaled image after erosion
    gray_preprocessed = erode_img(gray_preprocessed)    # Erode the grayscaled image
    
    # Apply Gaussian blur to smooth out the edges
    blur = cv2.GaussianBlur(gray_preprocessed, (3, 3), 0)
    
    # check to see if we should apply thresholding to preprocess the image
    if preprocess_type == "thresh":
        preprocessed_img = cv2.threshold(blur, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Saving the preprocessed image
    output_dir = os.path.join(output_path, os.path.splitext(os.path.basename(filename))[0])
    preprocessed_img_dir = os.path.join(output_dir, "preprocessed_image_files")
    
    # Check if the sub directory (preprocessed_image_files) exists, if not then create one. Else continue
    if not os.path.exists(preprocessed_img_dir):
        os.mkdir(preprocessed_img_dir)
    
    original_img_filename = os.path.splitext(os.path.basename(filename))[0]
    img_filename = "{}_{}.png".format(original_img_filename + "_preprocessed", page_num)
    preprocessed_img_path = os.path.join(preprocessed_img_dir, img_filename)    
    cv2.imwrite(preprocessed_img_path, preprocessed_img)
    
    return preprocessed_img

def apply_OCR(gray_preprocessed):
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to the input grayscaled image
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
    output_dir = os.path.join(output_path, os.path.splitext(os.path.basename(filename))[0])
    all_pages = wi(filename= f"{output_dir}.pdf", resolution=resolution)
    
    # print(os.path.exists(output_dir))
    # Check if an output directory exists, if not then create one. Else continue
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    # Move input file into the output directory
    shutil.move(f"{output_path}\\{filename}", f"{output_dir}\\{filename}") 
    
    image_file_dir = os.path.join(output_dir, "image_files")
    # Check if the sub directory (image_files) exists, if not then create one. Else continue
    if not os.path.exists(image_file_dir):
        os.mkdir(image_file_dir)
    
    for i, page in enumerate(all_pages.sequence, start=1):
        with wi(page) as img:
            img.format = "png"
            img.background_color = wc("white")
            img.alpha_channel = "remove"

            image_filename = os.path.splitext(os.path.basename(filename))[0]
            image_filename = f"{image_filename}_{i}.png"
            image_filename = os.path.join(image_file_dir, image_filename)
            
            img.save(filename=image_filename)

def save2Txt(filename, page_num, extracted_text, output_path):
    ''' Takes in the extracted text from an image 

        Create a subdirectory (text_files) if it does not exist

        Write the extracted text to a text file which has the same name 
        as the correspending page of the PDf
    '''
    output_dir = os.path.join(output_path, os.path.splitext(os.path.basename(filename))[0])
    text_file_dir = os.path.join(output_dir, "text_files")
    
    # Check if the sub directory (text_files) exists, if not then create one. Else continue
    if not os.path.exists(text_file_dir):
        os.mkdir(text_file_dir)
    
    text_filename = os.path.splitext(os.path.basename(filename))[0]
    text_filename = f"{text_filename}_{page_num}.txt"
    textFile_path = os.path.join(text_file_dir, text_filename)
    
    with open(textFile_path, 'w') as txtFile:
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
        convert_pdf(path_to_pdf, PDF_DIR)  # A list of images converted from the input pdf 
    
    images_path = os.path.join(PDF_DIR, os.path.splitext(os.path.basename(args["pdf"]))[0])   
    images_path = os.path.join(images_path, "image_files")        
    images_list = os.listdir(images_path)
    images_list_sorted = sort_image_list(images_list)
    
    for page_num, img_name in enumerate(images_list_sorted, start=1):
        print(f"++++++++++++++++++++++++++++++ page {page_num} ++++++++++++++++++++++++++++++")
        
        img_path = os.path.join(images_path, img_name)
        # Load and read image using cv2
        image, gray = load_img(img_path)
        
        # Preprocess the gray image we obtained earlier
        gray_preprocessed = preprocess_img(args["pdf"], PDF_DIR, page_num, args["preprocess"], gray)
        
        # Store the text extracted from the image
        text_extracted = apply_OCR(gray_preprocessed)
        print(text_extracted)
        
        # Save extracted page content into its corresponding .txt file
        save2Txt(args['pdf'], page_num, text_extracted, PDF_DIR)
        
        print("++++++++++++++++++++++++ End of page ++++++++++++++++++++++++")
        print('')
        
        # **Optional** Display original image and preprocessed image
        display_imgs(image, gray_preprocessed, args["displayIMGs"])
    
if __name__ == "__main__":
    main()