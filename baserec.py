import os
import re
import math
import pandas as pd
import numpy as np
import pyspark as ps
from pyspark.mllib.recommendation import ALS
from pyspark import SparkContext, SparkConf
from pyspark.mllib.clustering import KMeans
#extremely rough code, jumping off point



def cluster_case(tfidf, n):
    cluster_model = KMeans.train(tfidf, n)
    centriods = cluster_model.centers
    return centriods

if __name__ == '__main__':

    training_RDD, validation_RDD, test_RDD = small_data.randomSplit([6, 2, 2], seed=0L)



    # seed =
    # iterations =
    # regularization_parameter =
    # ranks = []
    # errors = []
    # err =
    # tolerance =

    min_error = float('inf')
    best_rank = -1
    best_iteration = -1
    for rank in ranks:
        model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                          lambda_=regularization_parameter)
        predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
        rates_and_preds = validation_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
        error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
        errors[err] = error
        err += 1
        print 'For rank %s the RMSE is %s' % (rank, error)
        if error < min_error:
            min_error = error
            best_rank = rank

    print 'The best model was trained with rank %s' % best_rank
