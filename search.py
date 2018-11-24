#!/usr/bin/env python3

# Search Module
#
# The sole purpose of this module is to prompt the user for an query to search in the
# database. The query will be searched for in the database and prints the Top 10 links
# associated with the search query, along with the tf-idf scoring and the document ID.


# Import Libraries
from tokenizer import tokenize_text
import json
import os

# Directory for webpages
webpages_directory = '/Users/angel/Documents/GitHub/search_engine/webpages/WEBPAGES_RAW/'

# File name for JSON file containing URL for each document
bookkeeping_file = 'bookkeeping.json'

# File name for Database
database = "inverted_Index.txt"


def get_Top(query, index):
    query = query.lower()
    tokens = set(tokenize_text(query))

    results = {}
    
    for token in tokens:
        for key, value in index[token].items():
            results.update({key: value})

    results = sorted(results.items(), key=lambda x: x[1], reverse=True)[:10]
        
    return results
        

def get_results(top, bookkeeping):
    print("\nTop 10 matched URL's:")
    for i, key in enumerate(top, 1):
        print("#{}: {}".format(i, bookkeeping[key[0]]))
    print("\n")
    
    
    
def search():
    # Read bookkeeping files. Will be used to return links.
    with open(os.path.join(webpages_directory, bookkeeping_file), 'r') as file:
        bookkeeping = json.load(file)

    with open(database, 'r') as file:
        index = json.load(file)
    
    while True:
        query = input("Please input your search query: ")

        if query != '':
            top_links = get_Top(query, index)
            get_results(top_links, bookkeeping)

