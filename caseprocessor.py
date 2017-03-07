from pymongo import MongoClient
from unidecode import unidecode
from string import punctuation
from string import printable
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

def init_mongodb():
    #Mongo database and table
    db_client = MongoClient()
    db = db_client['case_database']
    coll = db.cases
    return db.cases

def nlp_case(incase, intest):
    '''
    note: need to add specialized stop words still
    '''
    tfidf = TfidfVectorizer(stop_words='english', max_df=.8, min_df=.01)
    vect= tfidf.fit_transform(incase)
    vtest= tfidf.transform(intest)
    clf = MultinomialNB(alpha=0.1)
    clf.fit(vect,y)
    df_pred=clf.predict(vtest)
    return None

def clean_text(text):
    clean = ''
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

if __name__ == '__main__':
    cases = init_mongodb()
    #should this include case ref?
    curs = cases.find() #cursor object
    dlist = list(curs)
    crefs = set()
    for i in dlist:
        for k,v in i.items():
            for v in i['case_ref']:
                if len(v)< 30:
                    x = v.strip()
                    crefs.add(x)
            i['case_text']= clean_text(i['case_text'])
