import os
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

load_dotenv()
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def search_tweet(hashtag):
    url = f'https://api.x.com/2/tweets/search/recent?query=%23{hashtag}&max_results=1'

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    response = requests.get(url, auth=auth)
    response_json = response.json()
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response_json)
    # Check for successful response
    if response.status_code == 200:
        tweets = response.json()
        tweet_count = len(tweets.get('data', []))  # Get the count of tweets
        print(f'Number of tweets found: {tweet_count}')
    else:
        print(f'Error: {response.status_code} - {response.text}')

def get_tweet_metrics(tweet_id):
    url = f'https://api.twitter.com/2/tweets/{tweet_id}'
    params = {
        'tweet.fields': 'public_metrics,non_public_metrics'
    }

    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    response = requests.get(url, auth=auth, params=params)
    response_json = response.json()
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response_json)

    if response.status_code != 200:
        print(f"Request returned an error: {response.status_code} {response.text}")
        return None

    if 'errors' in response_json:
        print("Errors in response:", response_json['errors'])
        return None

    if 'data' not in response_json:
        print("The 'data' field is missing in the response.")
        return None

    tweet_data = response_json['data']
    public_metrics = tweet_data.get('public_metrics', {})
    non_public_metrics = tweet_data.get('non_public_metrics', {})

    like_count = public_metrics.get('like_count', 0)
    impression_count = non_public_metrics.get('impression_count', 'Not available')

    return {
        'like_count': like_count,
        'impression_count': impression_count
    }

def post_tweet(content):
    # Define the endpoint for posting a tweet
    url = 'https://api.twitter.com/2/tweets'
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

    # Define the tweet content
    tweet_content = {
        "text": content
    }

    # Make the POST request to post the tweet
    response = requests.post(url, json=tweet_content, auth=auth)

    # Check if the request was successful
    if response.status_code == 201:
        print("Tweet posted successfully!")
        print(response.json())
    else:
        print("Failed to post tweet.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

    return response.json()