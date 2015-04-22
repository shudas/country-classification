# Country Classification
# Classifying a Twitter user's country of origin based on their tweets
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

Must have installed the python-twitter API wrapper: https://github.com/bear/python-twitter

getTweets.py:
	- This program basically gathers out data set (a bunch of tweets)
	- Each time this program is ran, it is ran for a specific country and a specific location 
	  within that country
	- To change the country, simply comment out the current country and uncomment out
	  the next country
	- To change the locations within a country, simply change the geo_index variable

	Run this program with the command:
	python getTweets.py

	The program will create and write to anywhere between 0-100 files, depending on the amount 
	of users tweeting in that location at runtime. The program creates these files within a 
	certain folder (ex. All_DATA/USA/) based on the country for that run. The files names are
	users and the content are that user's most recent tweets. The program writes around 90 
	tweets per user.
	

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

getStatistics.py:
	- This program can be run anytime after the data has been collected
	- It gets various statistics on the data set

	Run this program with the command:
	python getStatistics.py

	This program will output:
		1. The total number of tweets collected for each country
		2. The total number of users that tweets were collected from for each country
		3. The average number of tweets per user for each country
