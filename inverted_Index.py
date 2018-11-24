# Inverted Index Module
#
# This module will be implemented with the help of BeautifulSoup to facilitate
# parsing HTML. 


# Import Libraries and Functions
from tokenizer import tokenize_text
from bs4 import BeautifulSoup
import json
import math
import re
import os

# Check to see if <html> tag exists in document
html_exists = re.compile(r'<html[^<>]*>', re.IGNORECASE)

# Used to filter nested tags
filter_tags = re.compile(r'<.*?>')

# Function that will parse HTML
def parse_HTML(html):
    # List containing the parsed html. Parsed html will be tokenized.
    parsed_html = []
    full_text = ''
    # Check to see if 'html' is found within document; if not, return empty list.
    if html_exists.search(html) is None:
        return parsed_html

    # Parser helper that will allow me to filter tags and find text.
    soup = BeautifulSoup(html, 'html.parser')

    # Iterate through all the tags found in html
    for tag in soup.findAll(True, recursive = False):
            # Filter the text from tag and combine it.
            # (Example: <H1> Click <a href> Here </a> </H1> -> 'Click here'
            text = ' '.join(tag.findAll(text = True)).strip()

            # Filter out nested tags
            text = filter_tags.sub('', text)

            # Add all text to string to tokenize after loop
            full_text = full_text + " " + text
    
    parsed_html = tokenize_text(full_text)
  

    return parsed_html


# Creates an Index containing each word found in a document
# Stored in a dictionary as followed: {token: {doc_ID: freq, doc_ID: freq}}
def create_Index(directory, json_file):
    # Inverted Index (Dictionary: {token: freq}
    index = {}

    # Dictionary containing a count for the number of documents a token is found in.
    # Example: {server: 15}
    token_doc = {}
    
    # Navigate to directory with webpages, and read bookkeeping.json file.
    with open(os.path.join(directory, json_file), 'r') as file:
        bookkeeping = json.load(file)

    # Sort the documents by their path
    documents = sorted(bookkeeping.keys())

    # Number of Documents
    documents_Count = len(documents)

    # Iterate through each of the documents and tokenize the text.
    for i, document in enumerate(documents, 1):
        # Read current document
        with open(os.path.join(directory, document), 'r',  encoding="utf8") as doc:
            html = doc.read()

        # Parse the html content
        parsed_html = parse_HTML(html)

        # Print to console percentage of documents that have been parsed and tokenized.
        print('\t[{:.2%}] {:8d} token(s) from doc: {:10s}'.format(i / documents_Count, len(parsed_html), document))

        # Iterate through all tokens in parsed_html and add the freq and docuent in which the token was found in
        # Example: {token: {documend_ID: freq}}
        for token in parsed_html:
            if token in index:
                index[token].update({document: 1 + math.log10(parsed_html.count(token))})
            else:
                index[token] = {document: 1 + math.log10(parsed_html.count(token))}

            
            token_doc[token] = token_doc.get(token, 0) + 1;

    return index, documents_Count, token_doc

# Updates the index. We will update the index by replacing each the token frequency for tokens document
# to token frequency-inverse document frequency (tf-idf)
def update_Index(index, count, token_doc):
    # Place holder for each tokens idf
    idfs = {}

    # New index
    new_Index = {}

    # Calculate each tokens idf
    for token, doc_count in token_doc.items():
        idfs[token] = math.log10(count/doc_count)

    # Replace tf in index for tf-idf
    for token, docs in index.items():
        new_Index[token] = {}
        for key, value in docs.items():
            idf = idfs[token]
            tf_idf = idf * value
            new_Index[token].update({key: tf_idf})

    return new_Index
            
