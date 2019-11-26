#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application - Execute OCR and NLP analysis on user uploaded PDFs:
    
Usage:
    This script is called automatically whenever a user uploads a PDF file.

Options:
    -h, --help      Show this screen
    --version       Show version 
    --arg2 <key>    Extra argument [default: None]
'''

__author__ = "Eric Leung"
__copyright__ = "Copyright 2019, NLP project at PSP Investments"
__credits__ = ["Eric Leung", "spaCy", "Nic Schrading", "Dipanjan Sarkar"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Eric Leung / future interns"
__email__ = "Eleung@investpsp.ca"
__status__ = "Dev"

import os
import ocr
import nlp_preprocess

# Path to PDFs directory (Default)
PDF_DIR = '.\\PDF2News\\backend\\user_uploads'

def main(filename):
    ''' Main function 
    
    Application: Perform OCR text extraction and NLP analysis for user input file. 
                 Return Named Entities obtained from the corresponding file.
    '''
    
    file_extension = os.path.splitext(os.path.basename(filename))[1]
    # Check file format: If PDF: Convert PDF -> PNG; Else: Skip the conversion step
    if file_extension == ".pdf":
        ocr.convert_pdf(filename, PDF_DIR)
        
    # Getting the actual filename w/o extension
    images_path = os.path.join(PDF_DIR, os.path.splitext(os.path.basename(filename))[0])   
    images_dir = os.path.join(images_path, "image_files")        
    images_list = os.listdir(images_dir)
    images_list_sorted = ocr.sort_image_list(images_list)
    
    for page_num, img_name in enumerate(images_list_sorted, start=1):
        print(f"++++++++++++++++++++++++++++++ page {page_num} ++++++++++++++++++++++++++++++")
        # Load and read image using cv2
        image, gray = ocr.load_img(os.path.join(images_dir, img_name))
        
        # Preprocess the gray image we obtained earlier
        gray_preprocessed = ocr.preprocess_img(filename, PDF_DIR, page_num, 'thresh', gray)
        
        # Store the text extracted from the image
        text_extracted = ocr.apply_OCR(gray_preprocessed)
        print(text_extracted)
        
        # Save extracted page content into its corresponding .txt file
        ocr.save2Txt(filename, page_num, text_extracted, PDF_DIR)
        
        print("++++++++++++++++++++++++ End of page ++++++++++++++++++++++++")
        print('')

    
if __name__ == "__main__":
    filename = "sample.pdf"
    main(filename)