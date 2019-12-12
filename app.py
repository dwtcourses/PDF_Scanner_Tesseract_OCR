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

import ocr
import nlp_preprocess
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to PDFs directory (Default)
PDF_DIR = '.\\PDF2News\\backend\\pdfs'

# DB connection: 
db_string = 'postgres://postgres:El260720788!@localhost:5432/postgres'

# Create DB engine:
engine = create_engine(db_string)
session = sessionmaker(bind=engine)()
base = declarative_base()

class Pdf(base):
    __tablename__ = "Pdfs"
    
    # Fields
    id = Column(Integer, primary_key=True)
    sessionId = Column(String)
    fileLocation = Column(String)
    description = Column(String)
    tags = Column(String)
    createdAt = Column(Date)
    updatedAt = Column(Date)
    status = Column(String)
 
def readArgs():
    lines = sys.argv
    print(f"Arguments: {lines}")
    
readArgs()    
    
def getPdfs(fileformat: str):
    ''' Function to query all files in the "Pdfs" table 
        that matches the given file format
    
        Input: 
            sessionId - A string that represents the file format of the uploaded pdf file
        
        Output (Console):
            Prints out all files that matches the given file format.
    '''
    pdfs = session.query(Pdf) \
        .filter(Pdf.tags == fileformat) \
        .all()
    
    for pdf in pdfs:
        id = pdf.id
        sessionId = pdf.sessionId
        fileLocation = pdf.fileLocation
        description = pdf.description
        tags = pdf.tags
        createdAt = pdf.createdAt
        updatedAt = pdf.updatedAt
        status = pdf.status

        print(f"ID: {id} || Session ID: {sessionId} || File location: {fileLocation} || description: {description} || tags: {tags} || Created at: {createdAt} || Updated at: {updatedAt} || Status: {status} \n")
    
getPdfs('png')

def main(sessionId, filename):
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

    
# if __name__ == "__main__":
#     filename = "sample.pdf"
#     main(filename)
    
