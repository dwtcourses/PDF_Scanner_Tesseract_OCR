import plac
import os
import spacy
from spacy.matcher import PhraseMatcher
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

def printDirectory(path_to_directory:str=None):
    if not path_to_directory:
        print(os.listdir(os.getcwd()))
        return os.listdir(os.getcwd())
    else:
        print(os.listdir(path_to_directory))    
        return os.listdir(path_to_directory)
        
def get_textfiles(pdf_filename:str=None):
    ''' 
        Extracts text from textfiles 
        
        Args:
            pdf_filename: Name of the original PDF file that the texts extracted from. (Default value is None) 
            
        Output: 
            Returns a generator object contains text of each page
    '''
    if not pdf_filename:
        raise ValueError("Please pass a PDF filename.")
    
    dir_list = printDirectory()
    if pdf_filename not in dir_list:
        raise FileNotFoundError("Input file does not exist in the current directory.")
    else:
        texts = []
        dir_path = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdf_filename + "\\text_files") 
        text_files = os.listdir(dir_path)
        for f in text_files:
            text_filepath = os.path.join(dir_path, f)
            with open(text_filepath) as txtfile:
                text_in_page = txtfile.read()
                texts.append(text_in_page)
        return texts
    
    
       
    
    
    
    
    
    
        
''' Example:
    
label = 'CIADIR'
matcher = PhraseMatcher(nlp.vocab)
for i in ['Gina Haspel', 'Gina', 'Haspel',]:
    matcher.add(label, None, nlp(i))

one = nlp('Gina Haspel was nomiated in 2018')
matches = matcher(one)
print(matches)

'''







