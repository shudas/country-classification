import twitter




radius = '100mi'
append_or_write = 'w'

#geocode = (-35.465952,148.130035)  #Australia  ()-29.125106,121.533508  ()-16.732805,133.574523   ()-17.781963,143.813781  ()-20.120884,147.069168  ()-24.070149,148.936156  ()-27.928227,151.636046  ()-31.56534,150.261382  ()-35.465952,148.130035  #-36.585454,144.240875  #-34.099801,140.825499  #-24.140069,117.978514  #-24.932936,127.456054  #-28.851089,145.341796  #-23.892534,141.562499  #-26.365622,136.347654  #-29.624404,130.722654
#COUNTRY_FILE = 'AUSTRALIA'

#geocode = (57.15832,-4.465256)  #UK  ()52.401372,-3.004761  ()58.348905,-3.830567  ()57.984323,-4.645386  ()58.124078,-6.654053  ()57.48839,-4.929772  ()57.15832,-5.475998  ()57.15832,-4.465256  #57.466845,-3.67424  ()56.979145,-2.487717  #56.652316,-2.963219  #56.418185,-3.641281  #51.390328,-0.136643 #51.759034,-2.081223  #52.467422,0.138015  #52.992999,-1.257248  #53.870052,-1.476975  #54.614739,-2.103196  #55.495691,-2.784348  #55.928924,-4.146652
#COUNTRY_FILE = 'UK'

#geocode = (39.063508,-94.600526)  #USA   ()38.572387,-102.499695  ()45.327584,-122.670595  ()39.634544,-104.775238  ()33.603818,-112.079773  ()38.675385,-121.176454  ()32.794843,-96.786804  ()34.64595,-92.250825  ()39.063508,-94.600526  #39.595695,-86.108095  #40.936917,-81.581726  #40.433171,-79.922447  #41.892623,-74.111024  #37.469711,-77.463227  #33.713552,-84.262391  #30.285819,-81.713563  #38.459563,-90.152435  #44.924514,-93.315125  #44.035557,-103.171234
#COUNTRY_FILE = 'USA'

geocode = (45.172894,-77.319032)  #Canada   ()50.102328,-118.947601  ()50.760157,-114.333344  ()53.287613,-113.608247  ()52.007945,-106.972504  ()50.003571,-96.623383  ()47.15102,-71.869813  ()45.172894,-77.319032  #47.468279,-75.397797  #46.855757,-80.737152  #48.293498,-89.592133  #50.186816,-90.976411  #53.999406,-122.875902  #54.986501,-128.61557  #56.531682,-111.367036  #55.107946,-118.69011
COUNTRY_FILE = 'CANADA'


CONSUMER_KEY2 = "kgBHVR042PpBGr4OGLS2g6U9V"
CONSUMER_SECRET2 = "yCvjU9TQTWxvPFvILJ0FF5t9FHy43l7XV7jUh211h39RxQoksv"
ACCESS_KEY2 = "346746299-kR2pR6nRwAQW42PCnJtektnL2XxnmAS6GdL9TFBJ"
ACCESS_SECRET2 = "0YT8n960JHYARtBKF64qylRR8pc2pF2y8C5OT2U63FClU"

CONSUMER_KEY = "Hj5X7qrzG4QITijwSpQnwDhx7"
CONSUMER_SECRET = "jUjediEM5yu3w6lER0GURWyRJvDCrKwJ1F3TwsRLBlFx3DElGW"
ACCESS_KEY = "3064111864-ivc7ofpYWY1C4id2tsunSE4jLglqCAZ7pqTWlEx"
ACCESS_SECRET = "juV49AFalStDEJmJhAITPK8SvRvUV6HLyNzdEJ81c2t1p"

CONSUMER_KEY3 = "yUfy1krhS7QH4MIRgino2GWwg"
CONSUMER_SECRET3 = "VRgfJpiAqgQ5fODbMO9TFi9e0tQm8zAeqO0Wr1HI9iNAynxpgD"
ACCESS_KEY3 = "2896168672-AiFIfGCHHK9k0nT5JJ5ru7MZKWbacdunwlpwVY9"
ACCESS_SECRET3 = "awh4kjpM7g7D0camILSuKmqZ3OeayDyOMHLH8i4sWsnY8"

CONSUMER_KEY4 = "7YmJheHKKWcjvNK903v7kTnbp"
CONSUMER_SECRET4 = "agR5PFf4h7654qhqgbGDGva8eh0rR8YjDnDY7mbNhkBXrnZkHW"
ACCESS_KEY4 = "33133400-7LIrnIThjk9V9jqUxNVN526N8Vanfv6ErBOAuxYrq"
ACCESS_SECRET4 = "sTFJV9Qz32xVA7bwFjPJ1CnBKqsQb6DBoGoLtBPFrLQQC"

api = twitter.Api(consumer_key=CONSUMER_KEY4, consumer_secret=CONSUMER_SECRET4, access_token_key=ACCESS_KEY4, access_token_secret=ACCESS_SECRET4)

##rerunning this search multiple times in the same process returns the samtweets
##to get new tweets, we must restart the program.
tweets = api.GetSearch(term=None, geocode=(geocode[0], geocode[1],radius), count=100, lang='en')

valid_users = set()
## for now we just go through and assume all users are from whatever country we are searching
for tweet in tweets:
    valid_users.add(tweet.user.id)

all_tweets = {}
for uid in valid_users:
##    to specify the number of tweets returned per user, set count
    utweets = api.GetUserTimeline(user_id=uid, count=50, include_rts=False, exclude_replies=True, trim_user=True)
    all_tweets[uid] = ([i.text for i in utweets])

##write tweets out to file. this is in append mode so it will append to testTweetFile
for user, i in all_tweets.iteritems():
    try:
        f = open("NewData\\" + COUNTRY_FILE + "\\" + str(user), append_or_write)
        for tweet in i:
            f.write('%s\n' % tweet)
        f.close()
    except: #in case of unicode errors or other errors
        continue

