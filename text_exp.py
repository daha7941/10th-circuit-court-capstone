from caseprocessor import run_processor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

def main_exp(corpus, urefs):
    '''
    note: need to add (more?) specialized stop words still
    '''
    # more_words = ['court', 'defendants', 'defendant', 'plaintiffs', 'plaintiff', 'state', '10th', 'district', 'case', 'federal', 'mr', 'ms', 'dr', 'motion', 'evidence', 'jury', 'united', 'trial', 'ss', \
    # 'law', 'rule', 'claim', 'appeal', 'government']
    # more_sets = set(more_words)
    # my_stop_words = more_sets.union(urefs)
    # stop_words = text.ENGLISH_STOP_WORDS.union(my_stop_words)
    tfidf = TfidfVectorizer(stop_words=urefs, max_df=0.9, min_df=0.05)
    vectors = tfidf.fit_transform(corpus).toarray()
    return vectors
def top_words(tfidf, vectors, data, n):

    words = tfidf.get_feature_names()

    avg = np.sum(vectors, axis=0) / np.sum(vectors > 0, axis=0)
    print "top %d by average tf-idf" % n
    print get_values(avg, n, words)
    print

    total = np.sum(vectors, axis=0)
    print "top %d by total tf-idf" % n
    print get_values(total, n, words)
    print

def get_values(lst, n, labels):
    #sorts list and returns n values
    return [labels[i] for i in np.argsort(lst)[-1:-n-1:-1]]


def cos_corp(vectors, corpus):
    #find cosine similarity between all cases in the corpus
    cosine_similarities = linear_kernel(vectors, vectors)
    for i, case1 in enumerate(corpus):
        for j, case2 in enumerate(corpus):
            # limit prints to those above value and different cases
            if i != j:
                if cosine_similarities[i,j] > 0.9:
                    print i,j, cosine_similarities[i,j]

if __name__ == '__main__':
    out_dict, out_set = run_processor()

    #generate corpus
    corpus = []
    for item in out_dict:
        n = item['case_text']
        corpus.append(n)

    vect = main_exp(corpus,out_set)

    #top 20 words
    top_words(tfidf, vectors, corpus, 20)

    cos_corp(vectors, corpus)
