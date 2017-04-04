from ElasticSearchServices import ElasticSearchServices

#---- Elastic Search Details -------

index = "tweettrends"
collection = {
	"mappings": {
		"finaltweets2": {
			"properties": {
				"id": {
					"type": "string"
				},
                "source": {
					"type": "string"
				},
				"message": {
					"type": "string"
				},
				"author": {
					"type": "string"
				},
				"timestamp": {
					"type": "string"
				},
				"location": {
					"type": "geo_point"
				},
                "sentiment": {
					"type": "string"
				},
                "anger": {
					"type": "float"
				},
                "joy": {
					"type": "float"
				},
                "sadness": {
					"type": "float"
				},
                "fear": {
					"type": "float"
				},
                "disgust": {
					"type": "float"
				}
			}
		}
	}
}


#--------------------------------------------------------

try:
    collection_service = ElasticSearchServices()
    collection_service.create_collection(index, collection)
except:
    print "Index already created"

