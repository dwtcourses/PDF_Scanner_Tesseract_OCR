import spacy

nlp = spacy.load("en_core_web_sm")

def findWord(text, search_word="", print=True):
    '''
    This method takes in a text and convert it into a spacy Doc, return 
    all the words == search_word in the Doc. 
    '''
    doc = nlp(text)
    
    