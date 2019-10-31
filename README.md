# PDF_Scanner_Tesseract_OCR
NLP Project at PSP Investments

## Project Goals:

- **Entities extractions:** Getting useful information (such as People, Date, Location, Organizations, etc.) from raw data stored in PDFs.
- Create __semantic mappings__ between related entities.

## Business values:

* Replacing the tedious labor work of reading documents 
* Provide comprehensive summarization 
* Feature clustering 

---

## Approaches:
Before working on the NLP analysis part. We first need to implement a python script that is able to read in PDF files.

Originally, I had attempted to use various PDF parsers, libraries like: 


1. PyPDF2: a pure-python library that is built as a PDF toolkit, capable of extracting document information (title, author, …), splitting documents page by page, merging documents page by page, cropping pages, etc.

2. Tika-python: A Python port of the Apache Tika library that makes Tika available using the Tika REST Server.

However, all of the modules listed above won’t suit our use cases. Due to the fact that most of our input PDF files are generated from scanned documents instead of generated electronically.

---

## Solutions:

A solution would be instead of treating our input PDF files as traditional PDF files (electronically generated), we treat them as images (JPEG, PNG, etc.), and perform text detection on them.

![pdf-to-image](https://user-images.githubusercontent.com/30438439/67973504-0025b880-fbe7-11e9-9ff5-f7e9c865fd2c.png)


## Drawbacks:
Yet, there are some limitations to this method, the accuracy of the text extraction varies depending on the quality of the images. In order to improve the performance of our program, we may be required to train a custom machine learning model (a format specifically for PSP’s documents).


## Tesseract OCR – developed by google 

![google_ocr](https://user-images.githubusercontent.com/30438439/67974412-c8b80b80-fbe8-11e9-8de5-d9f7ec2a5b27.png)

* Tesseract is an optical character recognition engine for various operating systems. 

* It is free software, released under the Apache License, Version 2.0, and development has been sponsored by Google since 2006. 

* In 2006, Tesseract was considered one of the most accurate open-source OCR engines then available.


## Pytesseract
![tesseract_header](https://user-images.githubusercontent.com/30438439/67974538-0157e500-fbe9-11e9-814b-04a67fd79208.jpg)

* At the moment, I am using a library called pytesseract. 

* Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images. 

* Python-tesseract is a wrapper for Google's Tesseract-OCR Engine.


## Python program – quick walk through:
In the beginning, without any preprocessing on the input files, my program is able to read in PDFs and extract their content in an approximately 65-70% accuracy. 

Note: for electronically generated PDFs, the accuracy is ~100%.

THAT’S NOT GOOD ENOUGH! `:rage:`

![trash_data](https://user-images.githubusercontent.com/30438439/67975104-e8036880-fbe9-11e9-98d3-edf7290a888f.jpeg)

---

## Preprocessing the input PDFs:

In order to improve the accuracy of our program, it requires more pre-processing on the images before we extract the text from them. 

I will give a brief overview of how my program works below.

## Program pipeline:

1. Execute the python file (ocr.py)
2. Pass in the PDF filename under the flag *--pdf*
3. In this case, I am passing in a PDF file called *sample.pdf* which is located in the directoy called *pdf* (this is optional)

```bash
python .\ocr.py --pdf .\pdfs\sample.pdf
```

4. The program will automatically creates a folder, which named the same as the original PDF filename, under the “pdfs/converted_pdf_images” directory.


