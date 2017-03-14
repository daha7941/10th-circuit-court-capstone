import cPickle as pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

def main_exp():
    '''
    note: need to add (more?) specialized stop words still
    '''
    with open('case_pickle.txt','rb') as f:
        new_dict = pickle.load(f)
    with open('ref_pickle.txt','rb') as fp:
        new_set = pickle.load(fp)
    corpus = []
    for item in new_dict:
        n = item['case_text']
        corpus.append(n)
    # more_words = ['court', 'defendants', 'defendant', 'plaintiffs', 'plaintiff', 'state', '10th', 'district', 'case', 'federal', 'mr', 'ms', 'dr', 'motion', 'evidence', 'jury', 'united', 'trial', 'ss', \
    # 'law', 'rule', 'claim', 'appeal', 'government']
    # more_sets = set(more_words)
    # my_stop_words = more_sets.union(urefs)
    # stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)
    tfidf = TfidfVectorizer(stop_words=new_set, max_df=0.9, min_df=0.05, max_features=5000)
    vectors = tfidf.fit_transform(corpus)
    return tfidf, vectors, corpus

def top_words(tfidf, vectors, data, n):

    words = tfidf.get_feature_names()
    new_vect = vectors.toarray()
    avg = np.sum(new_vect, axis=0) / np.sum(new_vect > 0, axis=0)
    print "top %d by average tf-idf" % n
    print get_values(avg, n, words)
    print

    total = np.sum(new_vect, axis=0)
    print "top %d by total tf-idf" % n
    print get_values(total, n, words)
    print

def get_values(lst, n, labels):
    #sorts list and returns n values
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]]


def cos_corp(vectors, corpus):
    #find similarity between all cases in the corpus
    new_vect = vectors.toarray()
    similarities = linear_kernel(new_vect, new_vect)
    # for i, case1 in enumerate(corpus):
    #     for j, case2 in enumerate(corpus):

            # if i != j:
            #     print i,j, similarities[i,j]
    return similarities
if __name__ == '__main__':

    tfidf, vectors, corpus = main_exp()

    #top 20 words
    top_words(tfidf, vectors, corpus, 20)

    m = cos_corp(vectors, corpus)
