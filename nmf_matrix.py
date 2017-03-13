from caseprocessor import run_processor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def nmf_topic_matrix(corpus, urefs, id_list):
    tfidf = TfidfVectorizer(stop_words=urefs, max_df=0.9, min_df=0.05,max_features=5000)
    tfidf_vectors = tfidf.fit_transform(corpus)
    dm = tfidf_vectors.toarray()
    vcb = np.array(tfidf.get_feature_names())
    nmf = NMF(n_components= 10,random_state=1, alpha=0.1, l1_ratio=0.5)
    case_topic = nmf.fit_transform(dm)

    case_topic = case_topic / np.sum(case_topic, axis=1, keepdims=True)
    id_list = np.asarray(id_list)
    case_topic_ori = case_topic.copy()
    num_groups = len(id_list)
    case_topic_grouped = np.zeros((num_groups, 10))
    for i, case in enumerate(id_list):
        case_topic_grouped[i,:]=np.mean(case_topic[id_list==case,:],axis=0)
    return case_topic_grouped

if __name__ == '__main__':
    out_dict, out_set = run_processor()

    #generate corpus
    corpus = []
    id_list = []
    for item in out_dict:
        n = item['case_text']
        case_id = item['_id']
        corpus.append(n)
        id_list.append(case_id)

    matz = nmf_topic_matrix(corpus, out_set, id_list)
    test_df = pd.DataFrame(matz, index = id_list)
    test_df['class']=test_df.idxmax(axis=1)
    
