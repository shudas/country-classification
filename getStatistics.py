import os
import glob

# where all the data is located
dataFolder = "ALL_DATA"
countryFolders = ["AUSTRALIA", "CANADA", "UK", "USA"]

# used to track how many users and total tweets
tweetCounts = {"AUSTRALIA": 0, "CANADA": 0, "UK": 0, "USA": 0}
userCounts = {"AUSTRALIA": 0, "CANADA": 0, "UK": 0, "USA": 0}

for country in countryFolders:
	# the names of the files are the user ids
	users = glob.glob(dataFolder + os.sep + country + os.sep + "*")
	# go through each file (user) and increment the user count for that country
	for user in users:
		userCounts[country] += 1
		f = open(user, 'r')
		lines = f.readlines()

		# go through each line (tweet) and increment the tweet count for that country
		for line in lines:
			if line != '\n':
				tweetCounts[country] += 1
		f.close()

# output statistics
for country, count in tweetCounts.iteritems():
	print "Number of " + country + " Tweets: " + str(count)
print
for country, count in userCounts.iteritems():
	print "Number of " + country + " users: " + str(count)
print
for country, count in tweetCounts.iteritems():
	print "Average Number of Tweets per User in " + country + ": " + str(count/userCounts[country])