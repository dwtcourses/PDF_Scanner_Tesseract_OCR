import os
import string
import spacy
from spacy.lang.en import English
import nltk
from nltk.corpus import state_union, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Default pdf directory
CONVERTED_PDF_IMAGE_DIR = ".\\pdfs\\converted_pdf_images"

# Load spaCy english small model
nlp = spacy.load("en_core_web_sm")

'''Auxilary functions 
'''
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

def clean_text (text):
    # Tokenize the input text 
    tokens = word_tokenize(text)
    
    # Convert all words/tokens to lowercase
    tokens = [w.lower() for w in tokens]
    
    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    print(words)
    


pdfs_dir = os.listdir(CONVERTED_PDF_IMAGE_DIR)[0]
pdf_file_dir = os.path.join(CONVERTED_PDF_IMAGE_DIR, pdfs_dir)
pdf_files = os.listdir(pdf_file_dir)
text_files_dir = os.path.join(pdf_file_dir, "text_files")
text_files = os.listdir(text_files_dir)
text_files = sort_file_list(text_files)

input_file_path = os.path.join(text_files_dir, text_files[0])
# ent_list = findEnts(input_file_path)

with open(input_file_path) as textFile:
    text = textFile.read()
    clean_text(text)


# # Testing NLTK  
# with open(input_file_path) as textFile:
#     text = textFile.read()
    
#     tokenized = word_tokenize(text)
#     # print(tokenized)
#     stop_words = set(stopwords.words('english'))
    
#     filtered_sentence = [w for w in tokenized if not w in stop_words]    
#     tagged = nltk.pos_tag(filtered_sentence[40:70]) 
#     print(tagged)
    
#     namedEnt = nltk.ne_chunk(tagged)
#     namedEnt.draw()

    
