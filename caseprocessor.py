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

def nlp_case(file):
    return None

def clean_text(text):
    clean = ''
    for char in text:
        if char in printable and char not in punctuation:
            clean += char.lower()
    return clean

def text_processing(dlist):
    #changes input from list of dictionaries to a string 
    new_list = []
    for i in dlist:
        new_list.append(i.values()[0])
    temp = map(unidecode, new_list)
    tdf = map(clean_text,temp)
    return " ".join(tdf)

if __name__ == '__main__':
    cases = init_mongodb()
    curs = cases.find({},{'case_text':True, '_id':False}) #cursor object
    dlist = list(curs)
    #
    df = text_processing(dlist)
    # indf = df.index.values
    '''
    note: need to add specialized stop words still
    '''
    tfidf = TfidfVectorizer(stop_words='english', max_df=.8, min_df=.01)
    # vect= tfidf.fit_transform(df['doc'])
    # vtest= tfidf.transform(df['doc'])
    # clf = MultinomialNB(alpha=0.1)
    # clf.fit(vect,y)
    # df['NB_pred']=clf.predict(vtest)
