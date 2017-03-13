import sys
import pandas as pd
from pymongo import MongoClient
from unidecode import unidecode
from string import punctuation
from string import printable
from multiprocessing import Pool, cpu_count
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


def clean_text(case_dict):
    case_text = case_dict['case_text']
    crefs = set(map(unidecode, (x.lower() for x in case_dict['case_ref'])))
    more_words = ['court', 'defendant', 'plaintiff', 'state', '10th', 'district', 'case', 'federal', 'mr', 'ms', 'dr', 'motion', 'evidence', 'jury', 'united', 'trial', 'ss', \
        'law', 'rule', 'claim', 'appeal', 'government','judgment', 'order', 'action', 'right', 'summary', 'testimony','judge']
    more_sets = set(more_words)
    my_stop_words = more_sets.union(crefs)
    new_stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)

    clean = ''
    # new_text = unidecode(case_text)
    for char in case_text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    token_text = nlp(clean)
    case_tokens = [token.lemma_ for token in token_text]
    case_dict['case_text'] = ' '.join(x for x in case_tokens if x not in new_stop_words)
    return case_dict

def clean_refs(multi_ref):
    set_refs = set()
    for r in multi_ref:
        if len(r)<30:
            r=r.strip().lower()
            set_refs.add(unidecode(r))
    return set_refs

def run_processor():
    cases = init_mongodb()
    curs = cases.find() #cursor object
    dlist = list(curs)
    pool = Pool(processes=cpu_count()-1)
    temp_res = pool.map(clean_refs, (i['case_ref'] for i in dlist))
    crefs = set.union(*temp_res)
    case_args = [(i['case_text'] for i in dlist), crefs]
    new_dlist = pool.map(clean_text, (d for d in dlist))
    # for i in dlist:
        # for k,v in i.items():
        # for v in i['case_ref']:
        #     if len(v)< 30:
        #         x = v.strip().lower()
        #         crefs.add(unidecode(x))
        # i['case_text']= clean_text(i['case_text'], crefs)
    # urefs = map(unidecode, crefs)
    return new_dlist, crefs
# def make_df(out_dict, out_set):
#     new_dict = {}
#     case_id = []
#     for i in out_dict:
#         new_key = i['_id']
#         new_val = i['case_ref']
#         new_dict.update({new_key:new_val})
#     df = pd.DataFrame.from_dict(new_dict, orient='index')
#     return df
if __name__ == '__main__':
    out_dict, out_set = run_processor()
    # case_df = make_df(out_dict, out_set)
