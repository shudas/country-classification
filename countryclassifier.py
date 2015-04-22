# Cultural Classification of Tweets
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

import sys, re, math, operator
from os import listdir
from os.path import isfile, join
from stemmer import PorterStemmer

trainingFolder = sys.argv[1]
folder = sys.argv[2]

# Set these parameters to change classifier performance
ngram = 1  #Up to 3
removeHashtags = True
removeNumbers = True
removeUsernames = False
removeStop = True
stem = False

def tokenizeText(inString):
    inString = inString.lower()

    # Remove non-unicode characters
    inString = re.sub(r'[^\x00-\x7F]+', ' ', inString)

    # Remove HTML special characters
    inString = re.sub('&[A-Za-z0-9]+;', ' ', inString)

    # Remove URLs
    inString = re.sub('http://t\.co/[A-Za-z0-9]+', ' ', inString)
    inString = re.sub('https://t\.co/[A-Za-z0-9]+', ' ', inString)

    # Remove Twitter usernames (optional)
    if removeUsernames:
        inString = re.sub('@[A-Za-z0-9_]+', ' ', inString)

    # Remove unnecessary characters
    inString = re.sub('[\\\!@%\^&\*(){}\[\]\|;:<>"\?~_\+=/\.,]', ' ', inString)

    # Remove Twitter hashtags (optional)
    if removeHashtags:
        inString = re.sub('#', ' ', inString)

    # Remove numbers (optional)
    if removeNumbers:
        inString = re.sub('\s[0-9]+\s', ' ', inString)

    # Parsing apostrophes
    inString = re.sub(r'([A-Za-z]+)\'([A-Za-z]+)', r'\1\2', inString)
    inString = re.sub(r'([A-Za-z]+)\'', r'\1', inString)
    inString = re.sub('\'', ' ', inString)

    # Only remove '-' if there are two of them consecutively or a space follows or precedes
    inString = re.sub('--', ' ', inString)
    inString = re.sub(r'([A-Za-z0-9])- ', r'\1 ', inString)
    inString = re.sub(r' -([A-Za-z0-9])', r' \1', inString)
    inString = re.sub('\s-\s', ' ', inString)

    # Split up tweets if using bigrams or trigrams
    if ngram > 1:
        inString = re.sub('\n', ' --- ', inString)

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


#----------------------------------------------------------------------

def trainNaiveBayes(countries):
    classProbs = {}
    wordProbs = {}
    text = {}

    totalFiles = 0.0

    for country in countries:
        countryFiles = [f for f in listdir(join(trainingFolder,country)) if isfile(join(trainingFolder,country,f))]
        totalFiles += len(countryFiles)

        for myFile in countryFiles:
            className = country

            # Update class counts
            if className in classProbs:
                classProbs[className] += 1.0
            else:
                classProbs[className] = 1.0

            with open(trainingFolder + country + "/" + myFile, 'r') as f:
                data = f.read()

                # Preprocess text
                data = tokenizeText(data)
                if removeStop:
                    data = removeStopwords(data)
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
        classProbs[c] = classProbs[c]/totalFiles

    vocabulary = {}
    n = {}

    for c in text:
        wordProbs[c] = {}
        n[c] = 0
        for x in range(0, len(text[c])):
            word = text[c][x]

            # Form ngram for training
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
                    word2 = text[c][x+1]
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

    # Calculate Naive Bayes ngram values
    for c in wordProbs:
        for word in wordProbs[c]:
            wordProbs[c][word] = (wordProbs[c][word] + 1)/(n[c] + vocabSize)

    return classProbs, wordProbs, vocabSize, n


def testNaiveBayes(filename, classProbs, wordProbs, vocabSize, n, country):
    with open(folder + country + "/" + filename, 'r') as f:
        data = f.read()
        data = tokenizeText(data)
        if removeStop:
            data = removeStopwords(data)
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

            # Form the n-gram for testing
            if ngram == 1:
                gram = word

            if ngram == 2:
                if x+1 < len(data):
                    word2 = data[x+1]
                    gram = " ".join([word, word2])
                else:
                    continue

            if ngram == 3:
                if x+2 < len(data):
                    word2 = data[x+1]
                    word3 = data[x+2]
                    gram = " ".join([word, word2, word3])
                else:
                    continue

            # Use logs to avoid tiny values
            if gram in wordProbs[c]:
                p += math.log10(wordProbs[c][gram])
            else:
                p += math.log10(1.0/(n[c] + vocabSize))
        probs[c] = math.log10(classProbs[c]) + p

    v = list(probs.values())
    k = list(probs.keys())

    return k[v.index(max(v))]

# Manages the menu for running the program and for removing countries from classification consideration
def getCountries():
    selectedCountries = ["AUSTRALIA", "CANADA", "UK", "USA"]
    user_input = -1
    while user_input != 0:
        print "Selected countries:",
        for country in selectedCountries:
            print country,
        print
        print "Please select an option: \n   0. Run\n   1. Remove AUSTRALIA"
        print "   2. Remove CANADA\n   3. Remove USA\n   4. Remove UK"
        user_input = int(raw_input("Option: "))
        if user_input == 0:
            print "\n"
            break
        elif user_input == 1:
            selectedCountries = [f for f in selectedCountries if f != "AUSTRALIA"]
        elif user_input == 2:
            selectedCountries = [f for f in selectedCountries if f != "CANADA"]
        elif user_input == 3:
            selectedCountries = [f for f in selectedCountries if f != "USA"]
        elif user_input == 4:
            selectedCountries = [f for f in selectedCountries if f != "UK"]
        else:
            print "Please select a valid option."
        print "\n"

    print "Running cultural classifier on",
    size_limit = len(selectedCountries)
    counter = 0
    for country in selectedCountries:
        
        if counter != (size_limit - 1):
            print country,
            print "and",
        else:
            print country + "...",
        counter += 1
    return selectedCountries

#----------------------------------------------------------------------

# Main
if __name__ == "__main__":
    userSelectedCountries = getCountries()
    countryFolders = [f for f in listdir(folder) if f in userSelectedCountries]
    classProbs, wordProbs, vocabSize, n = trainNaiveBayes(countryFolders)

    testFolders = [f for f in listdir(folder) if f in userSelectedCountries]
    total = 0.0
    correct = 0.0
    correctLineNumbers = []
    incorrectLineNumbers = []

    # Predict for each test file
    for country in testFolders:
        testFiles = [f for f in listdir(join(folder,country)) if isfile(join(folder,country,f))]
        for testFile in testFiles:
            with open(join(folder,country,testFile)) as f:
                for i, l in enumerate(f):
                    pass
            numLines = i + 1
            prediction = testNaiveBayes(testFile, classProbs, wordProbs, vocabSize, n, country)
            total += 1.0
            if prediction == country:
                correctLineNumbers.append(numLines)
                correct += 1.0
            else:
                incorrectLineNumbers.append(numLines)

    print "\n\nAccuracy:", correct/total
    #print "Average number of tweets for corrects: ", reduce(lambda x, y: x + y, correctLineNumbers) / len(correctLineNumbers)
    #print "Average number of tweets for incorrects: ", reduce(lambda x, y: x + y, incorrectLineNumbers) / len(incorrectLineNumbers)
    #print

    # Print top words for each country
    for c in wordProbs:
        print c
        sorted_x = sorted(wordProbs[c].items(), key=operator.itemgetter(1), reverse=True)
        for x in range(0,10):
            print sorted_x[x]
