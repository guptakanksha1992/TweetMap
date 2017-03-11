# Here is where we can store and seach for tweets from the document

from ElasticSearchServices import ElasticSearchServices

class TwitterHandler:

	def __init__(self):
		self.es = ElasticSearchServices()
		self.index = "finaltwittermapindex5"
		self.doc_type = "finaltweets2"

	def getTweets(self, keyword):
		body = {
			"query": {
				"match": {
					"_all": keyword
				}
			}
		}

		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)
		print 'hey i am akanksha '+result
		return result

	def getTweetsWithDistance(self, keyword, distance, latitude, longitude):
		distance_string = distance + 'km'
		print distance_string
		body = {
			"query": {
				"match": {
					"_all": keyword
				}
			},
			"filter": {
				"geo_distance": {
					"distance": distance_string,
					"distance_type": "sloppy_arc",
					"location": {
						"lat": latitude,
						"lon": longitude
					}
				}
			}
		}

		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)

		return result

	def insertTweet(self, id, location_data, tweet, author, timestamp):
		print "!!!!!!!!!!!!!!!!"
		print id
		print tweet
		print author
		print timestamp
		print location_data[0]
		print location_data[1]
		body = {
			"id": id,
			"message": tweet,
			"author": author,
			"timestamp": timestamp,
			"location": location_data
		}

		result = self.es.store_data(self.index, self.doc_type, body)

		return result

