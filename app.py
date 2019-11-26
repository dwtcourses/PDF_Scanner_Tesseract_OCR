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
import requests

# Path to PDFs directory (Default)
PDF_DIR = '.\\PDF2News\\backend\\pdfs'

def main():
   pass
    
if __name__ == "__main__":
    main()
