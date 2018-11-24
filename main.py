#!/usr/bin/env python3

# Directory for webpages
webpages_directory = '/Users/angel/Documents/GitHub/search_engine/webpages/WEBPAGES_RAW/'

# File name for JSON file containing URL for each document
bookkeeping_file = 'bookkeeping.json'

# File name for Database
database = "inverted_Index.txt"

# Import Libraries and Functions
from tokenizer import tokenize_text
from inverted_Index import parse_HTML, create_Index, update_Index
from search import search
import json
import os

def create_Index():
    # Create inverted index
    print("Creating inverted index...")
    index, document_Count, token_doc= create_Index(webpages_directory, bookkeeping_file)

    # Updating inverted index
    print("\nUpdating inverted index...")
    index = update_Index(index, document_Count, token_doc)

    # Write inverted index into file
    print("\nWriting inverted index into file...")
    with open(database, 'w') as file:
        json.dump(index, file)

    print(
    '\nStatistics:\n'
    '    - Number of documents: {}\n'
    '    - Number of unique tokens: {}\n'
    '    - Database size on disk: {} KB\n\n'.format(
        document_Count, len(index), round(os.path.getsize(database)*0.0009765625))
    )
            
def main():
    # If database file does not exists, create it. Else, prompt user for query
    if os.path.isfile(database):
        search()
    else:
        create_Index()
        search()


        

if __name__ == '__main__':
    main()

