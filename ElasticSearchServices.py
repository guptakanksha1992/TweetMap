# This is the file where we connect to ES + find and insert data

from elasticsearch import Elasticsearch

# Our elastic search engine
HOSTADDRESS='search-tweetmap-whpei25apwtxe7bvkmaj34ozee.us-west-1.es.amazonaws.com'


class ElasticSearchServices:

    def __init__(self):
        self.es = Elasticsearch(
        		[HOSTADDRESS]

        	)

    def store_data(self, index, doc_type, body):
        results = self.es.index(
    			index=index,
    			doc_type=doc_type,
    			body=body
    		)

        return results

    def create_collection(self, index, body):
        print ("Creating collection...")
        results = self.es.indices.create(
            index=index,
            body=body
        )
        return results

    def search(self, index, doc_type, body, size):
    	results = self.es.search(
    			index = index,
    			doc_type = doc_type,
    			body = body,
    			size = size
    		)

    	return results;

    def total_hits(results):
    	return results['hits']['total']

