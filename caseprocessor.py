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

def nlp_case(corpus, urefs):
    '''
    note: need to add specialized stop words still
    '''
    more_words = ['court', 'defendants', 'defendant', 'plaintiffs', 'plaintiff']
    more_sets = set(more_words)
    my_stop_words = more_sets.union(urefs)
    stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)
    tfidf = TfidfVectorizer(stop_words=stop_words)
    vectors = tfidf.fit_transform(corpus).toarray()


    # vtest= tfidf.transform(intest)
    # clf = MultinomialNB(alpha=0.1)
    # clf.fit(vect,y)
    # df_pred=clf.predict(vtest)
    return None

def clean_text(text):
    clean = ''
    text = unidecode(text)
    for char in text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    return clean

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
    #generate corpus
    # corpus = []
    # for item in dlist:
    #     n = item['case_text']
    #     corpus.append(n)
    return dlist, urefs

if __name__ == '__main__':
    out_dict, out_set = run_processor()
