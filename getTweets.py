import twitter
import os

# Where the tweets are written to
folder_name = "ALL_DATA"
radius = '50mi'

# COUNTRIES

# To change countries, comment out the current country and uncomment out the next.
# Then, increment the geo_index for the next country to change the geolocation

# Australia locations
geocode = [(-29.125106,121.533508), (-16.732805,133.574523), (-17.781963,143.813781), (-20.120884,147.069168), (-24.070149,148.936156), (-27.928227,151.636046), (-31.56534,150.261382), (-35.465952,148.130035), (-36.585454,144.240875), (-34.099801,140.825499), (-24.140069,117.978514), (-24.932936,127.456054), (-28.851089,145.341796), (-23.892534,141.562499), (-26.365622,136.347654), (-29.624404,130.722654), (-34.951648,138.631668), (-33.900468,151.167068)]
COUNTRY_FILE = 'AUSTRALIA'
geo_index = 16  # indexes into geocode

# UK locations
'''geocode = [(52.401372,-3.004761), (58.348905,-3.830567), (57.984323,-4.645386), (58.124078,-6.654053), (57.48839,-4.929772), (57.15832,-5.475998), (57.15832,-4.465256), (57.466845,-3.67424), (56.979145,-2.487717), (56.652316,-2.963219), (56.418185,-3.641281), (51.390328,-0.136643), (51.759034,-2.081223), (52.467422,0.138015), (52.992999,-1.257248), (53.870052,-1.476975), (54.614739,-2.103196), (55.495691,-2.784348), (55.928924,-4.146652)]
#COUNTRY_FILE = 'UK'
#geo_index = 12  # indexes into geocode   '''

# USA locations
'''geocode = [(38.572387,-102.499695), (45.327584,-122.670595), (39.634544,-104.775238), (33.603818,-112.079773), (38.675385,-121.176454), (32.794843,-96.786804), (34.64595,-92.250825), (39.063508,-94.600526), (39.595695,-86.108095), (40.936917,-81.581726), (40.433171,-79.922447), (41.892623,-74.111024), (37.469711,-77.463227), (33.713552,-84.262391), (30.285819,-81.713563), (38.459563,-90.152435), (44.924514,-93.315125), (44.035557,-103.171234)]
#COUNTRY_FILE = 'USA'
#geo_index = 3  # indexes into geocode    '''

# Canada locations
'''geocode = [(50.102328,-118.947601), (50.760157,-114.333344), (53.287613,-113.608247), (52.007945,-106.972504), (50.003571,-96.623383), (47.15102,-71.869813), (45.172894,-77.319032), (47.468279,-75.397797), (46.855757,-80.737152), (48.293498,-89.592133), (50.186816,-90.976411), (53.999406,-122.875902), (54.986501,-128.61557), (56.531682,-111.367036), (55.107946,-118.69011)]
#COUNTRY_FILE = 'CANADA'
#geo_index = 1  # indexes into geocode    '''




# KEYS are the various access tokens and such. Each team member got their own 
# tokens so that this script could be run more often without hitting the Twitter API request limit
KEYS =[["kgBHVR042PpBGr4OGLS2g6U9V", "yCvjU9TQTWxvPFvILJ0FF5t9FHy43l7XV7jUh211h39RxQoksv", "346746299-kR2pR6nRwAQW42PCnJtektnL2XxnmAS6GdL9TFBJ", "0YT8n960JHYARtBKF64qylRR8pc2pF2y8C5OT2U63FClU"], 
       ["Hj5X7qrzG4QITijwSpQnwDhx7", "jUjediEM5yu3w6lER0GURWyRJvDCrKwJ1F3TwsRLBlFx3DElGW", "3064111864-ivc7ofpYWY1C4id2tsunSE4jLglqCAZ7pqTWlEx", "juV49AFalStDEJmJhAITPK8SvRvUV6HLyNzdEJ81c2t1p"], 
       ["yUfy1krhS7QH4MIRgino2GWwg", "VRgfJpiAqgQ5fODbMO9TFi9e0tQm8zAeqO0Wr1HI9iNAynxpgD", "2896168672-AiFIfGCHHK9k0nT5JJ5ru7MZKWbacdunwlpwVY9", "awh4kjpM7g7D0camILSuKmqZ3OeayDyOMHLH8i4sWsnY8"], 
       ["7YmJheHKKWcjvNK903v7kTnbp", "agR5PFf4h7654qhqgbGDGva8eh0rR8YjDnDY7mbNhkBXrnZkHW", "33133400-7LIrnIThjk9V9jqUxNVN526N8Vanfv6ErBOAuxYrq", "sTFJV9Qz32xVA7bwFjPJ1CnBKqsQb6DBoGoLtBPFrLQQC"]]
# Change key_index each time the program is run to evenly cycle through the access tokens
# values: 0, 1, 2, 3
key_index = 3




# establish connection
api = twitter.Api(consumer_key=KEYS[key_index % len(KEYS)][0], consumer_secret=KEYS[key_index % len(KEYS)][1], access_token_key=KEYS[key_index % len(KEYS)][2], access_token_secret=KEYS[key_index % len(KEYS)][3])

# retrieve the most recent 100 tweets from a certain latitude and longitude
tweets = api.GetSearch(term=None, geocode=(geocode[geo_index][0], geocode[geo_index][1],radius), count=100, lang='en')

# from those tweets, get the user ids
valid_users = set()
for tweet in tweets:
    valid_users.add(tweet.user.id)

# go through the user id's tweets and grab their most recent tweets
all_tweets = {}
for uid in valid_users:
    # to specify the number of tweets returned per user, set count
    utweets = api.GetUserTimeline(user_id=uid, count=200, include_rts=False, exclude_replies=True, trim_user=True)
    all_tweets[uid] = ([i.text for i in utweets])

# write tweets out to file. this is in append mode so it will append to testTweetFile
for user, i in all_tweets.iteritems():
    try:
        f = open(folder_name + os.sep + COUNTRY_FILE + os.sep + str(user), 'w')
        for tweet in i: #in case of unicode errors
            try:
                f.write('%s\n' % tweet.encode('utf8'))  # write tweet to file
            except:
                print "unicode error " + tweet.encode('utf8')
                continue
        f.close()
    except: #in case of file errors
        print "file error"
        continue

