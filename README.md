# Country Classification
# Classifying a Twitter user's country of origin based on their tweets
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

Must have installed the python-twitter API wrapper: https://github.com/bear/python-twitter

getTweets.py:



partitionAllData.py:
	- This program should be run before running either of the following classifier files
	- Uses the ALL_DATA folder to create two new folders, TEST and TRAIN
	- 20% of the data files will be in TEST, other 80% will be in TRAIN
	- This fraction can be modified by changing the test_percentage variable in the code

	Run this program with the command:
	python partitionAllData.py     

	There is no output for this program.


countryclassifier.py:
	- Trains and tests a Naive Bayes classifier
	- First command line argument specifies the folder to be used for training the classifier
	- Second command line argument specifies the folder to be used for testing the classifier
	- Variables listed at the top of the program can be changed to impact classifier performance (ex: choosing to remove hashtags or not)

	Run this program with the command:
	python countryclassifier.py TRAIN/ TEST/

	This program will output the overall accuracy of the classifier as well as the top 10 words for each class.


countryclassifier_svm.py:
-execute 'module load python' before running on CAEN 
-set normalizeMatrix, tfidf parameters before running 
