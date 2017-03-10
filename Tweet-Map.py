
# coding: utf-8

# In[1]:

import tweepy


# In[9]:

auth = tweepy.OAuthHandler('uJ8ywVGKTC7aubwomDuWrAu9t', 'qbcDPiGjdNGj3B2EiXja3z0ppxMenePTzp6X1nAur2CakwLF1G')
auth.set_access_token('3287103102-m7iUaz9H6eOmgl50DBMXPfePIywVFEnYldLAUoa', 'lrJiIAcGZRvxPNTTvo5TCe3KRJp6FaqNZGIOC0SSOHLsx')
 
api = tweepy.API(auth)
 
api.update_status(status="Hello, world!")


# In[3]:

keyword_list = ['fun','apple','potato','football','orange','papaya','blue','wednesday','pikachu','times']


# In[4]:

keyword_list


# In[6]:

print api.trends_place(1)


# In[35]:

tweets = []

for i in range(10):

    tweets_keyword = tweepy.Cursor(api.search, q=keyword_list[i]).items(10)

    for tweet in tweets_keyword:
        tweets.append((tweet.text, tweet.geo))


# In[36]:

tweets


# In[ ]:

# Streaming API


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_status(self, status):
        # Prints the text of the tweet
        print('Tweet text: ' + status.text)
 
        # There are many options in the status object,
        # hashtags can be very easily accessed.
        for hashtag in status.entries['hashtags']:
            print(hashtag['text'])
 
        return true
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 
if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
 
    stream = Stream(auth, listener)
    stream.filter(follow=[38744894], track=['#pythoncentral'])

