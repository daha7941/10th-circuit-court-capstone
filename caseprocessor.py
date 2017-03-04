from pymongo import MongoClient
from string import punctuation
from string import printable
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def nlp_case(file):
    return None

def clean_text(text):
    clean = ''
    for char in text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    return clean

def text_processing(df):
    df['description'] = df['description'].map(clean_text)
    return df

if __name__ == '__main__':
    df = text_processing(dataf)
    indf = df.index.values
    y=df.pop('label').values
    '''
    note: need to add specialized stop words still
    '''
    tfidf = TfidfVectorizer(stop_words='english', max_df=.8, min_df=.01)
