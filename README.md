# Country Classification
# Classifying a Twitter user's country of origin based on their tweets
# Eric Riedel, Shu Das, Ross McKay, Lily Chen

Must have installed the python-twitter API wrapper: https://github.com/bear/python-twitter

getTweets.py:
	- This program was used to gather our data set (the tweets)
	- This program is run for a specific country and a specific location within that country
	- To change the country, comment out the current country and uncomment out the next country within the code
	- To change the locations within a country, change the geo_index variable

	Run this program with the command:
	python getTweets.py

	The program will create and write to anywhere between 0-100 files, depending on the amount 
	of users tweeting in the specified location at runtime. The program creates these files within a 
	certain folder (ex. All_DATA/USA/) based on the country for that run. The files names are
	user IDs and the content is that user's most recent tweets. The program writes around 90 
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
	- Trains and tests a Naive Bayes classifier on the given data
	- First command line argument specifies the folder to be used for training the classifier
	- Second command line argument specifies the folder to be used for testing the classifier
	- Variables listed at the top of the program can be changed to impact classifier performance (ex: choosing to remove hashtags or not)
	- References the code in stemmer.py when the word stemming option is turned on

	Run this program with the command:
	python countryclassifier.py TRAIN/ TEST/

	Upon running the program, the user will see a listing of options, which allows them
	to remove countries from consideration in the classification process. The default option
	is to run the classifier on all countries (US, UK, Canada, Australia), however any
	combination of these can be removed. Use option 0 to run the classifier once the desired
	country configuration is reached.

	This program will output the overall accuracy of the classifier as well as the top 10 words for each class.
	(More top words can be output by changing variables in the code.)


countryclassifier_svm.py:
	- Trains and tests a linear SVM classifier 
	- First command line argument specifies the folder to be used for training the classifier 
	- Second command line argument specifies the folder to be used for testing the classifier 
	- Variables at the top of can be used to specify the weighting scheme of the feature vectors used in the classifier
	  (i.e. tfidf, normalization, feature selection
	
	Run this program on CAEN with the command: 
	module load python 
	python countryclassifier_svm.py TRAIN/ TEST/ 

	This program will output the overall accuracy of the classifier. 

getStatistics.py:
	- This program can be run any time after the data has been collected
	- It provides various statistics on the data set

	Run this program with the command:
	python getStatistics.py

	This program will output:
		1. The total number of tweets collected for each country
		2. The total number of users that tweets were collected from for each country
		3. The average number of tweets per user for each country
