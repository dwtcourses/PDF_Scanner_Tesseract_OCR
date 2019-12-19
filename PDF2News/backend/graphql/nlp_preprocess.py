#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application - Extract named entities from unstructured try:
    
Usage:
    nlp_preprocess.py arg1 [--arg2 <key>]
    nlp_preprocess.py (-h | --help)
    nlp_preprocess.py --version

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
import sys
import string
import spacy
from spacy.matcher import PhraseMatcher
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokens import Span
import unicodedata
from contractions import CONTRACTION_MAP
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re

# Default PDFs directory
PDF_DIR = 'C:\\Users\\Administrator\\Desktop\\Eric\\pytesseract\\PDF2News\\backend\\pdfs\\'

# Load spaCy english small model
nlp = spacy.load("en_core_web_sm")

'''Auxilary functions 
'''
def sort_file_list(text_files) -> list:    
    # Sort the list of images by page number
    sorted_list = sorted(text_files, key=lambda n : int((n.split('_')[1][:-4])))
    return sorted_list

def offseter(lbl, doc, matchitem) -> tuple:
    o_one = len(str(doc[0:matchitem[1]]))
    subdoc = doc[matchitem[1]:matchitem[2]]
    o_two = o_one + len(str(subdoc))
    return (o_one, o_two, lbl)    

def get_directory_list(path_to_directory: str = None) -> list:
    ''' 
        Gets the list of files exist in the directory (if provided) or 
        the current directory
        
        Args: 
            path_to_directory: string (Default value: None)
        
        Output: 
            texts: list of strings
    '''
    if not path_to_directory:
        # print(os.listdir(os.getcwd()))
        return os.listdir(os.getcwd())
    else:
        # print(os.listdir(path_to_directory))    
        return os.listdir(path_to_directory)
        
def get_texts(pdf_filename: str = None, path_to_directory: str = None) -> object:
    ''' 
        Extracts text from textfiles 
        
        Args:
            pdf_filename: Name of the original PDF file that the texts extracted from. (Default value is None) 
            
        Output: 
            Returns a generator object contains text of each page
    '''
    if not pdf_filename:            # No input filename is given: raise Value error
        raise ValueError("Please enter a PDF filename.")
    
    if not path_to_directory:       # No input directory path: Search current directory
        dir_list = get_directory_list()
    else:
        dir_list = get_directory_list(path_to_directory)
    
    if pdf_filename not in dir_list:
        raise FileNotFoundError("Input file does not exist in the current directory.")
    else:
        dir_path = os.path.join(PDF_DIR, pdf_filename + "\\text_files") 
        text_files = os.listdir(dir_path)
        text_files = sort_file_list(text_files)     # Sort the list of files by page number
        
        for f in text_files:
            text_filepath = os.path.join(dir_path, f)
            with open(text_filepath) as txtfile:
                text_in_page = txtfile.read()
                yield text_in_page              # use generator to speed up process

def expand_contractions(text: str, contraction_mapper: dict = CONTRACTION_MAP) -> str:
    '''
    Application: Expands all contractions in input text.
    
    Args:
        text: str - Text with contractions in it.
        contraction_mapper: dict - A mapping for each contraction to their expanded form, created by Mr. Dipanjan Sarkar. 
        
    Output: 
        expanded_text: str - Text with all contractions expanded to their original form.
    '''
    contractions_pattern = re.compile(f"({'|'.join(contraction_mapper.keys())})", 
                                      flags = re.IGNORECASE | re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapper.get(match)\
                                if contraction_mapper.get(match)\
                                else contraction_mapper.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def convert_accented_chars(text: str) -> str:
    '''
    Application: Converts accented characters from input text
    
    Args:
        text: str - Text with accented characters in it.
        
    Output: 
        standardized_text: str - Standardized text contains only English characters.     
    '''
    standardized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return standardized_text  

def normalize_text(text: str, lowercase: bool = True) -> str:
    # Make sure text is nonempty 
    # if not text:
    #     raise ValueError("Input text cannot be empty!")    
    
    # Make text lowercase
    text = text.lower()
    return text
    
def extract_entities(text: str = None):
    normalized_text = normalize_text(text)
    doc = nlp(normalized_text)
    
    # Iterate over the entities
    for token in doc:  
        print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")  

# pdf_name = get_directory_list(PDF_DIR)[0]    
# path = os.path.join(PDF_DIR, pdf_name)
# texts = get_texts(pdf_filename=pdf_name, path_to_directory=PDF_DIR)    

# extract_entities(next(texts))

# with open('C:\\Users\\Administrator\\Desktop\\Eric\\pytesseract\\pdfs\\converted_pdf_images\\190916-VARSWAP-BARCLAYS-582619\\text_files\\190916-VARSWAP-BARCLAYS-582619_1.txt') as file:
#     text = file.read()
#     doc = nlp(text)
#     for token in doc:
#         print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")  
    
    

''' Example:
    
label = 'CIADIR'
matcher = PhraseMatcher(nlp.vocab)
for i in ['Gina Haspel', 'Gina', 'Haspel',]:
    matcher.add(label, None, nlp(i))

one = nlp('Gina Haspel was nomiated in 2018')
matches = matcher(one)
print(matches)

'''