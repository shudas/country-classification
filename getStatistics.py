import os
import glob

topFolder = "ALL_DATA"
countryFolders = ["AUSTRALIA", "CANADA", "UK", "USA"]

tweetCounts = {"AUSTRALIA": 0, "CANADA": 0, "UK": 0, "USA": 0}
userCounts = {"AUSTRALIA": 0, "CANADA": 0, "UK": 0, "USA": 0}

for country in countryFolders:
	users = glob.glob(topFolder + os.sep + country + os.sep + "*")
	for user in users:
		userCounts[country] += 1
		f = open(user, 'r')
		lines = f.readlines()
		for line in lines:
			if line != '\n':
				tweetCounts[country] += 1
		f.close()

for country, count in tweetCounts.iteritems():
	print "Number of " + country + " Tweets: " + str(count)
print
for country, count in userCounts.iteritems():
	print "Number of " + country + " users: " + str(count)
print
for country, count in tweetCounts.iteritems():
	print "Average Number of Tweets per User in " + country + ": " + str(count/userCounts[country])