# Cultural Classification of Tweets
# SVM classifier 
# must 'module load python' before running on CAEN
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

import sys, re, math, operator
from os import listdir
from os.path import isfile, join
from stemmer import PorterStemmer
from sklearn.svm import LinearSVC
import countryclassifier as cc
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.feature_selection import SelectPercentile, f_classif

#parameters to change classifier performance defined in countryclassifier.py
normalizeMatrix = True
tfidf = False
feature_selection = False

#in countryclassifer.py
# trainingFolder is first command line argument 
# testing folder is second command line argument 

#----------------------------------------------------------------------
#reads in training data folder and creates the dictionary of vocabulary
def createVocab():
    vocab = {}
    index = 0 
    subfolders = listdir(join(cc.trainingFolder)) 

    for sf in subfolders:
        for user_file in listdir(join(cc.trainingFolder, sf)):
            if isfile(join(cc.trainingFolder, sf, user_file)): 
                #extract raw content from text document 
                data = open(join(cc.trainingFolder, sf, user_file), 'r').read()

                #Preprocess text 
                data = cc.tokenizeText(data)
                if cc.removeStop:
                    data = cc.removeStopwords(data)
                if cc.stem:
                    data = cc.stemWords(data)

                #add words to the vocabulary 
                for token in data:
                    if token not in vocab:
                        vocab[token] = index
                        index += 1
    return vocab

#extracts feature array and a corresponding label array to the dataset
def extractFeatures(folder, vocab, languages):
    subfolders = listdir(join(cc.trainingFolder))

    #initialize the size of the feature matrix 
    num_users = 0 
    for sf in subfolders: 
        num_users += len(listdir(join(cc.trainingFolder, sf)))
    feature_matrix = np.zeros((num_users, len(vocab)))
    labels = np.array([])

    #calculate raw counts for words in each user file
    index = 0 
    for sf in subfolders: 
        sf_array = np.ones(len(listdir(join(cc.trainingFolder, sf)))) * languages[sf]

        #add in labels 
        labels = np.append(labels, sf_array)
        for user_file in listdir(join(cc.trainingFolder, sf)):
            #extract raw text from document
            data = open(join(cc.trainingFolder, sf, user_file), 'r').read()

            #Preprocess text 
            data = cc.tokenizeText(data)
            if cc.removeStop:
                data = cc.removeStopwords(data)
            if cc.stem:
                data = cc.stemWords(data)

            #update word counts in feature matrix
            for token in data: 
                if token in vocab: 
                    feature_matrix[index][vocab[token]] += 1
            index += 1

    return feature_matrix, labels 

#takes in a folder of user tweet files, does not have subfolders of labels 
#can be used to predict for individual users whose countries are unknown
#not actually used in main, but makes system robust so that a main can be called on 
#unlabled users 
def extractFeaturesDemo(usersFolder, vocab, languages):
    feature_matrix = np.zeros((len(listdir(join(usersFolder))), len(vocab)))
    print feature_matrix
    user_index = 0 
    for user_file in listdir(join(usersFolder)):             
        #extract raw text from document
        data = open(join(usersFolder, user_file), 'r').read()

        #Preprocess text 
        data = cc.tokenizeText(data)
        if cc.removeStop:
            data = cc.removeStopwords(data)
        if cc.stem:
            data = cc.stemWords(data)
        # print len(data) 
        for token in data: 
            if token in vocab: 
                #print token, vocab[token]
                feature_matrix[user_index][vocab[token]] += 1
        user_index += 1

    return feature_matrix

#----------------------------------------------------------------------
#Main
if __name__ == "__main__":
    languages = {
        'USA': 0,
        'UK': 1, 
        'AUSTRALIA': 2,
        'CANADA': 3
    }

    vocab = createVocab()
    print 'done vocab'
    training_feat, train_label = extractFeatures(cc.trainingFolder, vocab, languages)

    #extract labels from labeled test data 
    test_feat, test_label = extractFeatures(cc.folder, vocab, languages)

    #transform count matrix 
    if tfidf: 
        print 'tfidf'
        transformer = TfidfTransformer()
        training_feat = transformer.fit_transform(training_feat)
        test_feat = transformer.fit_transform(test_feat)
    if normalizeMatrix: 
        print 'normalize'
        training_feat = preprocessing.normalize(training_feat)
        test_feat = preprocessing.normalize(test_feat)
    if feature_selection:
        print 'feature selection'
        selector = SelectPercentile(f_classif, percentile=10)
        training_feat = selector.fit_transform(training_feat, train_label)
        test_feat = selector.transform(test_feat)

    print 'testing folder: ', cc.folder
    print 'training folder:', cc.trainingFolder
    clf = LinearSVC()
    clf.fit(training_feat, train_label)
    prediction = clf.predict(test_feat)
    print 'accuracy:', accuracy_score(prediction, test_label)

#-----------------------------------------------------------------------
