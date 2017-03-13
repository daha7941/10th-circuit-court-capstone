from text_exp import main_exp
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import numpy as np

def main_extra(vectors, tfidf, corpus):

    n_features= 5000
    #tf-idf for NMF
    # tfidf = TfidfVectorizer(stop_words=urefs, max_df=0.9, min_df=0.05,max_features=n_features)
    # tfidf_vectors = tfidf.fit_transform(corpus)

    #tf for LDA
    countvect = CountVectorizer(max_df=0.95, min_df=2,max_features=n_features)
    tf_vectors = countvect.fit_transform(corpus)

    nmf = nmf_model(vectors)
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

if __name__ == '__main__':
    tfidf, vectors, corpus = main_exp()

    main_extra(vectors, tfidf, corpus)
