import cPickle as pickle
import random
def make_sub(pickle_file):
    with open(pickle_file,'rb') as f:
        test_dict = pickle.load(f)
    return random.choice(test_dict)

if __name__ == '__main__':
    new_out = make_sub('case_test_pickle.txt')
