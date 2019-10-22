import os
import spacy
from spacy.lang.en import English
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Default pdf directory
CONVERTED_PDF_IMAGE_DIR = ".\\pdfs\\converted_pdf_images"

# Load spaCy english small model
nlp = spacy.load("en_core_web_sm")

def sort_file_list(text_files):    
    # Sort the list of images by page 
    sorted_list = sorted(text_files, key=lambda n : int((n.split('_')[1][:-4])))
    return sorted_list

def findEnts(file_path):
    '''
    findDates(text): 
        takes in a text and convert it into a spacy Doc, return all 
        the words == search_word in the Doc. 
    '''
    with open(file_path) as textFile:
        text = textFile.read()
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

pdfs_dir = os.listdir(CONVERTED_PDF_IMAGE_DIR)[0]
pdf_file_dir = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdfs_dir)
pdf_files = os.listdir(pdf_file_dir)
text_files_dir = os.path.join(pdf_file_dir, "text_files")
text_files = os.listdir(text_files_dir)
text_files = sort_file_list(text_files)

input_file_path = os.path.join(text_files_dir, text_files[4])
ent_list = findEnts(input_file_path)

for ent_tup in ent_list:
    print(ent_tup)