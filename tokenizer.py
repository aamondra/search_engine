# Tokenizer Module
#
# This module will be implemented using the NLTK Tokenization Library.


# Importing Libraries
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


# Creates a Lemmatizer helper function that will normalize words.
# Example: cats -> cat; cacti -> cactus, etc...
lemmatizer = WordNetLemmatizer().lemmatize

# Creates a tokenizer helper function that will create a list of words from a sentence.
tokenizer = RegexpTokenizer("[\w']+")

# Create a set containing english stopwords
stopwords = set(stopwords.words('english'))

# Defining a function that will tokenize a text. Returns a list of tokens.
def tokenize_text(text):
    # List of tokens that will be returned
    tokens = [];

    # Removes any non-alphabetic characters from the text.
    text = re.sub('[.]+', '', text)
    text = re.sub('[^a-zA-Z0-9]+', ' ', text)
    
    # A list of words found in the sentence
    words = tokenizer.tokenize(text)

    # Iterate through each of the words found in the text
    for word in words:
        # Normalize word by converting to all lowercase
        word = word.lower()
        
        # Filter out stopwords
        if word not in stopwords:
            tokens.append(lemmatizer(word))
    return tokens


