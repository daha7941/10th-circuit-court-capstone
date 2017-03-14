from text_exp import main_exp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import cPickle as pickle

def nmf_topic_matrix(corpus, vectors, tfidf):
    tfidf_vectors = vectors
    dm = tfidf_vectors.toarray()
    vcb = np.array(tfidf.get_feature_names())
    nmf = NMF(n_components= 10,random_state=1, alpha=0.1, l1_ratio=0.5)
    case_topic = nmf.fit_transform(dm)

    topic_corpus = top_words(nmf, vcb, 75)
    return case_topic, topic_corpus

def case_rec(case_topic, id_list):
    case_topic = case_topic / np.sum(case_topic, axis=1, keepdims=True)
    id_list = np.asarray(id_list)
    case_topic_ori = case_topic.copy()
    num_groups = len(id_list)
    case_topic_grouped = np.zeros((num_groups, 10))
    for i, case in enumerate(id_list):
        case_topic_grouped[i,:]=np.mean(case_topic[id_list==case,:],axis=0)
    return case_topic_grouped

def top_words(model, feature_names, n_words):
    topic_corpus = []
    for i, v in enumerate(model.components_):
        print ('Topic {0}').format(i)
        topic_text =(' '.join(feature_names[x] for x in v.argsort()[:-n_words - 1:-1]))
        topic_corpus.append(topic_text)
        # print topic_text
        print()
    return topic_corpus
if __name__ == '__main__':
    tfidf, vectors, corpus = main_exp()
    with open('case_pickle.txt','rb') as f:
        new_dict = pickle.load(f)
    id_list = []
    for item in new_dict:
        n = item['_id']
        id_list.append(n)


    case_topic, topic_corpus = nmf_topic_matrix(corpus, vectors, tfidf)
    case_matrix = case_rec(case_topic, id_list)
    test_df = pd.DataFrame(case_matrix)
    test_df['id']=id_list
    test_df['class']=test_df.idxmax(axis=1)
    test_df.to_csv('nmf_df.csv')
