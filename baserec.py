import numpy as np
import pandas as pd
import cPickle as pickle
from sklearn.metrics.pairwise import linear_kernel
from text_exp import main_exp
from take_sub import make_sub
from nmf_matrix import nmf_topic_matrix
'''need to loop through topic_corpus to find most similar topic then loop through docs within that topic'''
def find_term_matrix(tfidf, corpus):
    term_matrix = tfidf.transform(corpus)
    return term_matrix

def find_sim(tfidf, vectors, topic_corpus,test_corpus):
    topic_term_matrix = find_term_matrix(tfidf, topic_corpus)
    test_term_matrix = find_term_matrix(tfidf, test_corpus)
    similarities = linear_kernel(test_term_matrix,topic_term_matrix)
    return similarities

def find_case(df,y):
    some_num = int(y.values)
    new_df = df[df['class']==some_num]
    case_list = new_df['id'].tolist()
    return case_list
def find_similar_case(case_list_dict, case_list):
    sub_topic_corpus=[]
    for casedict in case_list_dict:
        for i in casedict.items():
            if i['_id'] in case_list:
                sub_topic_corpus.append(i['case_text'])
    return sub_topic_corpus

def final_rec(tfidf, vectors, sub_topic_corpus,case_text):
    sub_topic_term = find_term_matrix(tfidf, sub_topic_corpus)
    case_term =find_term_matrix(tfidf, case_text)
    sim = find_sim(tfidf, vectors, sub_topic_term,case_term)
    case_idx = sim.argmax()

if __name__ == '__main__':
    df = pd.read_csv('nmf_df.csv')

    with open('case_pickle.txt','rb') as f:
        case_list_dict = pickle.load(f)
    test_corpus=[]
    test_case = make_sub('case_test_pickle.txt')
    test_text= test_case['case_text']
    test_corpus.append(test_text)
    tfidf, vectors, corpus = main_exp()
    case_topic, topic_corpus = nmf_topic_matrix(corpus, vectors, tfidf)
    cosm = find_sim(tfidf, vectors, topic_corpus,test_corpus)
    topic_df = pd.DataFrame(cosm)
    topic_df['class']=topic_df.idxmax(axis=1)
    y = topic_df.pop('class')
    case_list = find_case(df,y)
    sub_topic_corpus =find_similar_case(case_list_dict, case_list)
    case_idx = final_rec(tfidf, vectors, sub_topic_corpus,test_corpus)
    recc = case_list_dict[case_idx]
    print recc['case_title']
