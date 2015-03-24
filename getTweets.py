import twitter



radius = '400mi'
append_or_write = 'w'
'''
geocode = (-26.519735,143.613281)  #Australia
fileName = 'Australia_tweets.txt'
'''

'''
geocode = (52.401372,-3.004761)  #UK
fileName = 'UK_tweets.txt'

geocode = (52.102288,5.866699)  #Netherlands
fileName = 'Netherlands_tweets2.txt'
'''
geocode = (38.572387,-102.499695)  #USA
fileName = 'USA_tweets.txt'
'''
geocode = (55.959282,-111.48377)  #Canada
fileName = 'Canada_tweets.txt'
'''




CONSUMER_KEY = "Hj5X7qrzG4QITijwSpQnwDhx7"
CONSUMER_SECRET = "jUjediEM5yu3w6lER0GURWyRJvDCrKwJ1F3TwsRLBlFx3DElGW"
ACCESS_KEY = "3064111864-ivc7ofpYWY1C4id2tsunSE4jLglqCAZ7pqTWlEx"
ACCESS_SECRET = "juV49AFalStDEJmJhAITPK8SvRvUV6HLyNzdEJ81c2t1p"
api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_KEY, access_token_secret=ACCESS_SECRET)

##rerunning this search multiple times in the same process returns the samtweets
##to get new tweets, we must restart the program.
tweets = api.GetSearch(term=None, geocode=(geocode[0], geocode[1],radius), count=100, lang='en')

valid_users = set()
## for now we just go through and assume all users are from whatever country we are searching
for tweet in tweets:
    valid_users.add(tweet.user.id)

all_tweets = []
for uid in valid_users:
##    to specify the number of tweets returned per user, set count
    utweets = api.GetUserTimeline(user_id=uid, count=50, include_rts=False, exclude_replies=True, trim_user=True)
    all_tweets.extend([i.text for i in utweets])

##write tweets out to file. this is in append mode so it will append to testTweetFile
with open(fileName, append_or_write) as f:
    for i in all_tweets:
        try:
            f.write('%s\n' % i)
        except: #in case of unicode errors or other errors
            continue

