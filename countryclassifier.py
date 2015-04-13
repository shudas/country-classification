# Cultural Classification of Tweets
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

import sys, re, math, operator
from os import listdir
from os.path import isfile, join
from stemmer import PorterStemmer

folder = sys.argv[1]
trainingFolder = "trainingData/"

# Set these parameters to change classifier performance
ngram = 1  #Up to 3
removeHashtags = False
removeNumbers = False
stem = False
removeStop = False
removeEmo = False

def tokenizeText(inString):
    inString = inString.lower()

    # Remove URLs
    inString = re.sub('http://t\.co/[A-Za-z0-9]+', ' ', inString)
    inString = re.sub('https://t\.co/[A-Za-z0-9]+', ' ', inString)

    # Remove Twitter usernames
    inString = re.sub('@[A-Za-z0-9_]+', ' ', inString)

    # Remove HTML special characters
    inString = re.sub('&[A-Za-z0-9]+;', ' ', inString)

    # Remove Twitter hashtags (optional)
    if removeHashtags:
        inString = re.sub('#[A-Za-z0-9_]+', ' ', inString)

    # Remove numbers (optional)
    if removeNumbers:
        inString = re.sub('\s[0-9]+\s', ' ', inString)

    # Remove unnecesary commas
    inString = re.sub('., ', ' ', inString)
    inString = re.sub(r'([A-Za-z]+),', r'\1 ', inString)

    # Removing unnecessary periods
    inString = re.sub('\s\.\s', ' ', inString)
    inString = re.sub(r'([0-9A-Za-z]+)\.\s', r'\1 ', inString)

    inString = re.sub(r'([A-Za-z]+)\.[0-9]', r'\1 ', inString)
    inString = re.sub(r'([0-9]+)\.[A-Za-z]', r'\1 ', inString)

    # Parsing apostrophes
    inString = re.sub(r'([A-Za-z]+)\'([A-Za-z]+)', r'\1\2', inString)
    inString = re.sub(r'([A-Za-z]+)\'', r'\1', inString)

    # Dealing with dates
    inString = re.sub('(?![0-9][0-9])/(?![0-9][0-9])', ' ', inString)

    # Only remove '-' if there are two of them consecutively or a space follows or precedes
    inString = re.sub('--', ' ', inString)
    inString = re.sub(r'([A-Za-z0-9])- ', r'\1 ', inString)
    inString = re.sub(r' -([A-Za-z0-9])', r' \1', inString)

    outList = inString.split()
    return outList

def removeStopwords(inList):
    with open('stopwords.txt') as f:
        stopwords = f.read().split()

    outList = [x for x in inList if x not in stopwords]
    return outList

def stemWords(inList):
    outList = []
    ps = PorterStemmer()

    for token in inList:
        stemmed_token = ps.stem(token, 0, len(token)-1)
        outList.append(stemmed_token)

    return outList

def removeEmoticons(inList):
    with open('emoticons.txt') as f:
        emoticons = f.read().split()

    outList = [x for x in inList if x not in emoticons]
    return outList


#----------------------------------------------------------------------

def trainNaiveBayes(files):
    classProbs = {}
    wordProbs = {}
    text = {}

    for myFile in files:
        # Change this line depending on format of data file names
        r = re.compile('([a-zA-Z]+)_[a-zA-Z0-9\.]+')
        m = r.match(myFile)
        className = m.group(1)

        # Update class counts
        if className in classProbs:
            classProbs[className] += 1.0
        else:
            classProbs[className] = 1.0

        with open(trainingFolder + myFile, 'r') as f:
            data = f.read()
            
            # Preprocess text
            data = tokenizeText(data)
            if removeStop:
                data = removeStopwords(data)
            if removeEmo:
                data = removeEmoticons(data)
            if stem:
                data = stemWords(data)

            # Extract text for particular class
            if className in text:
                text[className].extend(data)
                text[className].append('')
            else:
                text[className] = data
                text[className].append('')

    # Update from counts to probabilities
    for c in classProbs:
        classProbs[c] = classProbs[c]/len(files)

    vocabulary = {}
    n = {}

    for c in text:
        wordProbs[c] = {}
        n[c] = 0
        for x in range(0, len(text[c])):
            word = text[c][x]

            if ngram == 1:
                gram = word

            if ngram == 2:
                if x+1 < len(text[c]):
                    word2 = text[c][x+1]
                    gram = " ".join([word, word2])
                else:
                    continue
            
            if ngram == 3:
                if x+2 < len(text[c]):
                    word3 = text[c][x+2]
                    gram = " ".join([word, word2, word3])
                else:
                    continue

            n[c] += 1.0

            if gram in wordProbs[c]:
                wordProbs[c][gram] += 1.0
            else:
                wordProbs[c][gram] = 1.0

            if gram in vocabulary:
                vocabulary[gram] += 1.0
            else:
                vocabulary[gram] = 1.0

    vocabSize = len(vocabulary)

    for c in wordProbs:
        for word in wordProbs[c]:
            wordProbs[c][word] = (wordProbs[c][word] + 1)/(n[c] + vocabSize)

    return classProbs, wordProbs, vocabSize, n

def testNaiveBayes(filename, classProbs, wordProbs, vocabSize, n):
    with open(folder + filename, 'r') as f:
        data = f.read()
        data = tokenizeText(data)
        if removeStop:
            data = removeStopwords(data)
        if removeEmo:
            data = removeEmoticons(data)
        if stem:
            data = stemWords(data)
    
    data.append("")
    temp = ""
    data = [temp] + data

    probs = {}

    for c in classProbs:
        p = 0
        for x in range(0, len(data)):

            word = data[x]

            if ngram == 1:
                gram = word

            if ngram == 2:
                if x+1 < len(text[c]):
                    word2 = data[x+1]
                    gram = " ".join([word, word2])
                else:
                    continue

            if ngram == 3:
                if x+2 < len(text[c]):
                    word3 = data[c][x+2]
                    gram = " ".join([word, word2, word3])
                else:
                    continue

            if gram in wordProbs[c]:
                p += math.log10(wordProbs[c][gram])
            else:
                p += math.log10(1.0/(n[c] + vocabSize))
        probs[c] = math.log10(classProbs[c]) + p    

    v = list(probs.values())
    k = list(probs.keys())

    return k[v.index(max(v))]

#----------------------------------------------------------------------

# Main

trainingFiles = [f for f in listdir(trainingFolder) if isfile(join(trainingFolder,f))]
classProbs, wordProbs, vocabSize, n = trainNaiveBayes(trainingFiles)

testFiles = [f for f in listdir(folder) if isfile(join(folder,f))]

for testFile in testFiles:
    prediction = testNaiveBayes(testFile, classProbs, wordProbs, vocabSize, n)
    print ",".join([testFile, prediction])
