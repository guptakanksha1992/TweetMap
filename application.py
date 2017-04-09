import json
import thread
from flask_socketio import SocketIO, send, emit
from TweetListener import *
from flask import Flask, render_template, jsonify, request
from TweetHandler import TwitterHandler
import requests
import TweetPersister


# function that pulls tweets from twitter
def startTwitterRequests():
    startStream()

# EB looks for an 'application' callable by default.
application = Flask(__name__)
socketio = SocketIO(application)

@application.route('/')
def api_root():
    return render_template('index.html')
    # return 'Welcome'

@application.route('/search/<keyword>')
def searchKeyword(keyword):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweets(keyword)
    return jsonify(result)

@application.route('/search/<keyword>/<distance>/<latitude>/<longitude>')
def searchKeywordWithDistance(keyword, distance, latitude, longitude):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweetsWithDistance(keyword, distance, latitude, longitude)
    return jsonify(result)

# HTTP Endpoint for SNS
@application.route('/search/sns', methods = ['GET', 'POST', 'PUT'])
def snsFunction():
    try:
        # Notification received from SNS
        notification = json.loads(request.data)
    except:
        print("Unable to load request")
        pass

    headers = request.headers.get('X-Amz-Sns-Message-Type')
    print(notification)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
        print(url) 
    elif headers == 'Notification':
        TweetPersister.persistTweet(notification)
        socketio.emit('first', {'notification':'New Tweet!'})
    else: 
        print("Headers not specified")
 
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    thread.start_new_thread(startTwitterRequests, ())
    application.debug = True
    application.run()
    socketio.run(application, host = '0.0.0.0',debug=True, port=5000)