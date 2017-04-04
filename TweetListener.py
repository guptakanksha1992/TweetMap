#----------Parsing Configuration File--------------------

myvars = {}
with open("auth.txt") as myfile:
    for line in myfile:
        name, var = line.partition(":")[::2]
        myvars[name.strip()] = var.strip()

#----------Twitter API Details---------------------------

import tweepy
import json
from tweepy import Stream
from tweepy.streaming import StreamListener

consumerKey=myvars['twitter_consumer_key']
consumerSecret=myvars['twitter_consumer_secret']
accessToken=myvars['twitter_access_token']
accessSecret=myvars['twitter_access_secret']

#----------SQS Details---------------------------

import boto.sqs
from boto.sqs.message import Message

# Establishing Connection to SQS
conn = boto.sqs.connect_to_region("us-west-2", aws_access_key_id=myvars['aws_api_key'], aws_secret_access_key=myvars['aws_secret'])


KEYWORDS = ['Food', 'Travel', 'Hollywood', 'Art', 'Cartoons', 'Pizza', 'Friends', 'Miami']
REQUEST_LIMIT = 420

class TweetListener(StreamListener):
    def on_data(self, data):
        try:
            parse_data(data)
        except Exception,e:
            # print(data)
            print("No location data found" + e)

        return(True)

    def on_error(self, status):
        errorMessage = "Error - Status code " + str(status)
        print(errorMessage)
        if status == REQUEST_LIMIT:
            print("Request limit reached. Trying again...")
            exit()

def parse_data(data):
    print 'RAW DATA:',data  
    try:
    	json_data_file = json.loads(data)
    except Exception, e:
    	print 'Parsing failed'
    	print e
    # Could be that json.loads has failed

    print 'JSON DATA FILE:', json_data_file

    try:
        location = json_data_file["place"]
        coordinates = json_data_file["coordinates"]
    except Exception,e:
        print 'Location data parsing erroneous'
        print e

    # Setting location of the tweet

    if coordinates is not None:
        final_longitude = json_data_file["coordinates"][0]
        final_latitude = json_data_file["coordinates"][0]
    elif location is not None:
        coord_array = json_data_file["place"]["bounding_box"]["coordinates"][0]
        longitude = 0;
        latitude = 0;
        for object in coord_array:
            longitude = longitude + object[0]
            latitude = latitude + object[1]
        final_longitude = longitude / len(coord_array)
        final_latitude = latitude / len(coord_array)
    else:
    	# Insert code for random final_longitude, final_latitude here
        final_longitude=random.uniform(-180.0,180.0)
        final_latitude=random.uniform(-90.0, +90.0)
        
    tweetId = json_data_file['id_str']
    tweet = json_data_file["text"]
    author = json_data_file["user"]["name"]
    timestamp = json_data_file["created_at"]
    location_data = [final_longitude, final_latitude]

    # Tweet ready (without sentiment analysis by this point) - sending to queue

    print tweetId, location_data, tweet, author, timestamp

    try:
    	print 'Trying to publish to Queue the tweet', tweet
    	publishToQueue(tweetId, location_data, tweet, author, timestamp)
    except Exception, e:
    	print("Failed to insert tweet")
    	print str(e)

def publishToQueue(tweetId, location_data, tweet, author, timestamp):
	print 'In publishToQueue'
	q = conn.get_queue('tweet_queue')   # Connecting to the SQS Queue named tweet_queue
	m = Message()                       # Creating a message Object
	m.message_attributes = {
	    "id": {
	     "data_type": "String",
	     "string_value": str(tweetId)
	     },
	     "author": {
	         "data_type": "String",
	         "string_value": str(author)
	     },
	     "timestamp": {
	         "data_type": "String",
	         "string_value": str(timestamp)
	     },
	     "location": {
	        "data_type": "String",
	        "string_value": str(location_data)
	     }
	 }

	print 'Saving', tweet, 'as message body'
	m.set_body(tweet)

	try:
	    q.write(m)
	except Exception,e:
	    print 'Failed to publish to Queue'
	    print str(e)

def startStream():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    while True:
        try:
            twitterStream = Stream(auth, TweetListener())
            twitterStream.filter(track=KEYWORDS)
        except:
            print("Restarting Stream")
            continue

    #The location specified above gets all tweets, we can then filter and store based on what we want