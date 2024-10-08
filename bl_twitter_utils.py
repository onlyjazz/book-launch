import os

import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

load_dotenv()
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

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


def bold_header(text):
    """Convert the first line of a multiline text to bold Unicode characters."""
    bold_map = {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
        'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
        'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
        'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
        'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
        'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲',
        '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }

    # Split the text into lines
    lines = text.split('\n')

    # Convert only the first line to bold characters
    lines[0] = ''.join(bold_map.get(char, char) for char in lines[0])

    # Join the lines back together
    return '\n'.join(lines)