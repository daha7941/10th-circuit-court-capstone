from pymongo import MongoClient
from unidecode import unidecode
from string import punctuation
from string import printable
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text

def init_mongodb():
    #Mongo database and table
    db_client = MongoClient()
    db = db_client['case_database']
    coll = db.cases
    return db.cases

def nlp_case(incase, urefs):
    '''
    note: need to add specialized stop words still
    '''
    more_words = set('court', 'defendants', 'defendant', 'plaintiffs', 'plaintiff')
    my_stop_words = more_words.union(urefs)
    stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)
    tfidf = TfidfVectorizer(stop_words=stop_words, max_df=.8, min_df=.01)
    vect= tfidf.fit_transform(incase)
    # vtest= tfidf.transform(intest)
    clf = MultinomialNB(alpha=0.1)
    clf.fit(vect,y)
    # df_pred=clf.predict(vtest)
    return None

def clean_text(text):
    clean = ''
    text = unidecode(text)
    for char in text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    return clean

# def text_processing(case_text):
#     #changes input from list of dictionaries to a string
#     new_list = []
#     for i in case_text:
#         new_list.append(i)
#     # temp = map(unidecode, new_list)
#     tdf = map(clean_text,temp)
#     return " ".join(tdf)
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
                    crefs.add(x)
            i['case_text']= clean_text(i['case_text'])
    urefs = map(unidecode, crefs)
    return dlist, urefs

if __name__ == '__main__':
    out_dict, out_set = run_processor()
