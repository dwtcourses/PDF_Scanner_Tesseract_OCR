import plac
import os
import sys
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from pathlib import Path
import random 

# Default pdf directory
CONVERTED_PDF_IMAGE_DIR = ".\\pdfs\\converted_pdf_images\\"

# Load spaCy english small model
nlp = spacy.load("en_core_web_sm")

'''Auxilary functions 
'''
def sort_file_list(text_files):    
    # Sort the list of images by page number
    sorted_list = sorted(text_files, key=lambda n : int((n.split('_')[1][:-4])))
    return sorted_list

def offseter(lbl, doc, matchitem):
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
        
def get_textfiles(pdf_filename: str = None, path_to_directory: str = None):
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
        dir_path = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdf_filename + "\\text_files") 
        text_files = os.listdir(dir_path)
        text_files = sort_file_list(text_files)     # Sort the list of files by page number
        
        for f in text_files:
            text_filepath = os.path.join(dir_path, f)
            with open(text_filepath) as txtfile:
                text_in_page = txtfile.read()
                yield text_in_page              # use generator to speed up process
    
def preprocess_text():
     pass   
    
    
def extract_entities(text):
    doc = nlp(text)
    
    # Iterate over the entities
    for ent in doc.ents:
        # Print the entity text and label
        print(ent.text, ent.label_)
    


pdf_name = get_directory_list(CONVERTED_PDF_IMAGE_DIR)[0]    
path = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdf_name)
texts = get_textfiles(pdf_filename=pdf_name, path_to_directory=CONVERTED_PDF_IMAGE_DIR)    

extract_entities(next(texts))



''' Example:
    
label = 'CIADIR'
matcher = PhraseMatcher(nlp.vocab)
for i in ['Gina Haspel', 'Gina', 'Haspel',]:
    matcher.add(label, None, nlp(i))

one = nlp('Gina Haspel was nomiated in 2018')
matches = matcher(one)
print(matches)

'''


    
# def list_get_textfiles(pdf_filename: str = None, path_to_directory: str = None) -> list:
#     ''' 
#         Extracts text from textfiles 
        
#         Args:
#             pdf_filename: Name of the original PDF file that the texts extracted from. (Default value is None) 
            
#         Output: 
#             Returns a list of strings contains text of each page
#     '''
#     if not pdf_filename:            # No input filename is given: raise Value error
#         raise ValueError("Please pass a PDF filename.")
    
#     if not path_to_directory:       # No input directory path: Search current directory
#         dir_list = get_directory_list()
#     else:
#         dir_list = get_directory_list(path_to_directory)
    
#     if pdf_filename not in dir_list:
#         raise FileNotFoundError("Input file does not exist in the current directory.")
#     else:
#         dir_path = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdf_filename + "\\text_files") 
#         text_files = os.listdir(dir_path)
#         text_files = sort_file_list(text_files)
#         texts = []
#         for f in text_files:
#             text_filepath = os.path.join(dir_path, f)
#             with open(text_filepath) as txtfile:
#                 text_in_page = txtfile.read()
#                 texts.append(text_in_page)
#         return texts


# text_li = list_get_textfiles(pdf_name, CONVERTED_PDF_IMAGE_DIR)
    
# print(sys.getsizeof(texts))    
# print(sys.getsizeof(text_li))    
    
    







