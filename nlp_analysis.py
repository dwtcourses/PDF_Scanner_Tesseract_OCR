import spacy
from spacy.lang.en import English

nlp = English()

def findDates(text_list, search_word="", print=True):
    '''
    This method takes in a text and convert it into a spacy Doc, return 
    all the words == search_word in the Doc. 
    '''
    # Process the texts and print the adjectives
    
    # for doc in nlp.pipe(text_list):
    print(text_list[0])
    doc = nlp(text_list[0])
    # print([(ent.text, ent.label_) for ent in doc.ents if ent.label_ == "DATE"])
    
    