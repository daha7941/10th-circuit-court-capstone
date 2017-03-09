import sys
from pymongo import MongoClient
from unidecode import unidecode
from string import punctuation
from string import printable
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import spacy

if not 'nlp' in locals():
    nlp = spacy.load('en')

def init_mongodb():
    #Mongo database and table
    db_client = MongoClient()
    db = db_client['case_database']
    coll = db.cases
    return db.cases


def clean_text(case_text, crefs):
    more_words = ['court', 'defendants', 'defendant', 'plaintiffs', 'plaintiff', 'state', '10th', 'district', 'case', 'federal', 'mr', 'ms', 'dr', 'motion', 'evidence', 'jury', 'united', 'trial', 'ss', \
        'law', 'rule', 'claim', 'appeal', 'government']
    more_sets = set(more_words)
    my_stop_words = more_sets.union(crefs)
    new_stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)

    clean = ''
    new_text = unidecode(case_text)
    # case_text = nlp(case_text)
    # case_tokens = [token.lemma_.lower() for token in case_text]
    # return ' '.join(x for x in tokens if x not in new_stop_words)
    for char in case_text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    token_text = nlp(clean)
    case_tokens = [token.lemma_ for token in token_text]
    return ' '.join(x for x in case_tokens if x not in new_stop_words)

def run_processor():
    cases = init_mongodb()
    curs = cases.find() #cursor object
    dlist = list(curs)
    crefs = set()
    for i in dlist:
        for k,v in i.items():
            for v in i['case_ref']:
                if len(v)< 30:
                    x = v.strip().lower()
                    crefs.add(unidecode(x))
        i['case_text']= clean_text(i['case_text'], crefs)
    urefs = map(unidecode, crefs)
    #generate corpus
    # corpus = []
    # for item in dlist:
    #     n = item['case_text']
    #     corpus.append(n)
    return dlist, crefs

if __name__ == '__main__':
    out_dict, out_set = run_processor()
