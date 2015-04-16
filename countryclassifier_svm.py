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

#parameters to change classifier performance defined in countryclassifier.py
normalizeMatrix = False
tfidf = True

#----------------------------------------------------------------------
def createVocab():
    vocab = {}
    index = 0 
    subfolders = listdir(join(cc.trainingFolder)) 
    #print subfolders
    for sf in subfolders:
        for user_file in listdir(join(cc.trainingFolder, sf)):
            if isfile(join(cc.trainingFolder, sf, user_file)): 
                #extract raw content from text document 
                data = open(join(cc.trainingFolder, sf, user_file), 'r').read()

                #Preprocess text 
                data = cc.tokenizeText(data)
                if cc.removeStop:
                    data = cc.removeStopwords(data)
                if cc.removeEmo:
                    data = cc.removeEmoticons(data)
                if cc.stem:
                    data = cc.stemWords(data)

                for token in data:
                    if token not in vocab:
                        vocab[token] = index
                        index += 1
    return vocab

def extractFeatures(folder, vocab, languages):
    subfolders = listdir(join(cc.trainingFolder))

    num_users = 0 
    for sf in subfolders: 
        num_users += len(listdir(join(cc.trainingFolder, sf)))
    #print 'num_users', num_users
    feature_matrix = np.zeros((num_users, len(vocab)))
    labels = np.array([])

    index = 0 
    for sf in subfolders: 
        sf_array = np.ones(len(listdir(join(cc.trainingFolder, sf)))) * languages[sf]
        labels = np.append(labels, sf_array)
        for user_file in listdir(join(cc.trainingFolder, sf)):
            #extract raw text from document
            data = open(join(cc.trainingFolder, sf, user_file), 'r').read()

            #Preprocess text 
            data = cc.tokenizeText(data)
            if cc.removeStop:
                data = cc.removeStopwords(data)
            if cc.removeEmo:
                data = cc.removeEmoticons(data)
            if cc.stem:
                data = cc.stemWords(data)

            for token in data: 
                if token in vocab: 
                    feature_matrix[index][vocab[token]] += 1
            index += 1

    return feature_matrix, labels 

def extractFeaturesDemo(usersFolder, vocab, languages):
    #takes in a folder of just users, does not have subfolders of labels 

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
        if cc.removeEmo:
            data = cc.removeEmoticons(data)
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
def main():
    languages = {
        'USA': 0,
        'UK': 1, 
        'AUSTRALIA': 2,
        'CANADA': 3
    }

    vocab = createVocab()
    #print vocab
    training_feat, train_label = extractFeatures(cc.trainingFolder, vocab, languages)
    #extract labels from labeled test data 
    test_feat, test_label = extractFeatures(cc.folder, vocab, languages)

    if tfidf: 
        transformer = TfidfTransformer()
        training_feat = transformer.fit_transform(training_feat)
        test_feat = transformer.fit_transform(test_feat)

    if normalizeMatrix: 
        training_feat = preprocessing.normalize(training_feat)
        test_feat = preprocessing.normalize(test_feat)


    print 'testing folder: ', cc.folder
    print 'training folder:', cc.trainingFolder
    clf = LinearSVC()
    clf.fit(training_feat, train_label)
    prediction = clf.predict(test_feat)
    print 'accuracy:', accuracy_score(prediction, test_label)

main()
#-----------------------------------------------------------------------
