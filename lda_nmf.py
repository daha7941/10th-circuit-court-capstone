from text_exp import main_exp
from caseprocessor import run_processor
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np


def main_extra(corpus, urefs):

    n_features= 5000
    #tf-idf for NMF
    tfidf = TfidfVectorizer(stop_words=urefs, max_df=0.9, min_df=0.05,max_features=n_features)
    tfidf_vectors = tfidf.fit_transform(corpus)

    #tf for LDA
    countvect = CountVectorizer(stop_words=urefs, max_df=0.95, min_df=2,max_features=n_features)
    tf_vectors = countvect.fit_transform(corpus)

    nmf = nmf_model(tfidf_vectors)
    lda = lda_model(tf_vectors)

    tfidf_features = tfidf.get_feature_names()
    top_words(nmf, tfidf_features, 20)

    tf_features = countvect.get_feature_names()
    top_words(lda, tf_features,20)

def top_words(model, feature_names, n_words):
    for i, v in enumerate(model.components_):
        print ('Topic {0}').format(i)
        print(' '.join(feature_names[x] for x in v.argsort()[:-n_words - 1:-1]))
        print()

def nmf_model(tfidf_vectors):
    nmf = NMF(n_components= 10,random_state=1, alpha=0.1, l1_ratio=0.5)
    return nmf.fit(tfidf_vectors)


def lda_model(tf_vectors):
    lda = LatentDirichletAllocation(n_topics= 10, max_iter=15, learning_method = 'online', learning_offset=50., random_state=1)
    return lda.fit(tf_vectors)

def nmf_topic_matrix(corpus, urefs, id_list):
    tfidf = TfidfVectorizer(stop_words=urefs, max_df=0.9, min_df=0.05,max_features=5000)
    tfidf_vectors = tfidf.fit_transform(corpus)
    dm = tfidf_vectors.toarray()
    vcb = np.array(tfidf.get_feature_names())
    nmf = NMF(n_components= 10,random_state=1, alpha=0.1, l1_ratio=0.5)
    case_topic = nmf.fit_transform(dm)
    top_words(nmf, vcb, 20)
    case_topic = case_topic / np.sum(case_topic, axis=1, keepdims=True)
    id_list = np.asarray(id_list)
    case_topic_ori = case_topic.copy()
    num_groups = len(set(id_list))
    case_topic_grouped = np.zeros((num_groups, 10))
    for i, case in enumerate(sorted(set(id_list))):
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
    # main_extra(corpus,out_set)
    matz = nmf_topic_matrix(corpus, out_set, id_list)
