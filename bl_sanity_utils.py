from dotenv import load_dotenv
from datetime import datetime
import json

from requests import post, Response
import os
import requests
from bl_twitter_utils import post_tweet

# Load environment variables for global reference
load_dotenv()
project_id = os.getenv("SANITY_PROJECT_ID")
dataset = os.getenv("SANITY_DATASET")
token = os.getenv("SANITY_TOKEN")
api_version = os.getenv("SANITY_API_VERSION")

def update_post_tweet(doc_id, tweet_id):
    """
        Update a single post with tweet_id.
        :param doc_id:
        :param tweet_id:
        :return: 200 or failure and log_response
    """
    mutation = {
        "mutations": [
            {
                "patch": {
                    "id": doc_id,
                    "set": {
                        "tweet_id": tweet_id
                    }
                }
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = f"https://{project_id}.api.sanity.io/{api_version}/data/mutate/{dataset}"
    response = requests.post(url, json=mutation, headers=headers)
    log_query_response(' "patch": {"id": doc_id,"set": {"tweet_id": tweet_id}', response)
    return response.status_code


def insert_post(post_header, post_content):
    """
    Inserts a new post document into the Sanity Content Lake.

    Args:
    - document: The document to insert (should be a dictionary).

    Returns:
    - Response from the Sanity API.
    """

    url = f"https://{project_id}.api.sanity.io/{api_version}/data/mutate/{dataset}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    doc = {
        "_type": "post",
        "header": post_header,
        "draft": [
            {
                "_type": "block",
                "_key": "1",
                "children": [
                    {
                        "_type": "span",
                        "text": post_content,
                    }
                ]
            }
        ],
        "body": [
            {
                "_type": "block",
                "_key": "1",
                "children": [
                    {
                        "_type": "span",
                        "text": post_content,
                    }
                ]
            }
        ],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "cta": "https://www.amazon.com/Bob-Alice-anti-love-DANNY-LIEBERMAN-ebook/dp/B0DH83SGZ2/ref=sr_1_3"
    }
    # Wrap the document in the appropriate payload format
    payload = {
        "mutations": [
            {
                "create": doc
            }
        ]
    }

    # Make the POST request to insert the document
    response = post(url, headers=headers, data=json.dumps(payload))
    log_query_response(' "patch": {"create": doc)', response)
    return {response.status_code}


def query_sanity_documents(groq_query):
    url = f"https://{project_id}.api.sanity.io/{api_version}/data/query/{dataset}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response: Response = requests.get(url, params={"query": groq_query}, headers=headers)
    log_query_response(groq_query, response)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def log_query_response(groq_query: str, response: requests.Response) -> None:
    """
    Logs a query and its response status code.

    Parameters:
    groq_query (str): The GROQ query that was executed.
    response (requests.Response): The response object returned by the query.

    Returns:
    None
    """
    # Get the current timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Log the status code, URL, and content length for better clarity
    log_message = (
        f"Query ran at {current_timestamp} | Query: {groq_query} | "
        f"Returned Status: {response.status_code} | "
        f"Response Length: {len(response.text)}"
    )
    print(log_message)

def get_system_prompt():
    current_date = datetime.now()
    current_dow = current_date.isoweekday()
    # Query prompt documents by dow, body is portable text field, return a string
    query = f'*[_type == "prompt" && dow == {current_dow}]{{"body": pt::text(body)}}'
    data = query_sanity_documents(query)
    p = data['result'][0]['body']
    return p

def get_id_by_header(header):
    # Query prompt documents by dow, body is portable text field, return a string
    query = f'*[_type == "post" && header == "{header}"]'
    data = query_sanity_documents(query)
    return data['result'][0]['_id']

def get_post_by_header(header):
    # Query prompt documents by header
    # {{_id, header, approved, tweet_id, body: pt::text(body)}}
    query = f'*[_type == "post" && header == "{header}"]{{_id, header, approved, tweet_id, "body": pt::text(body)}}'
    data = query_sanity_documents(query)
    if data == 400:
       return None
    else:
        return data['result'][0]


def select_all(dataType):
    # Select _id and header fom dataType no WHERE clause, returns None if no tweet_id
    query = f'*[_type == "{dataType}"]{{_id, header, tweet_id}}'
    data = query_sanity_documents(query)
    return  data['result']


def sanity_to_x(content):
    """
    :type content: json array with _id header body portable text approved boolean tweet_id
    """
    doc_id = content["_id"]
    header = content['header']
    approved = content['approved']
    body = content['body']
    tweet_id = content['tweet_id']
    tweet = header + "\n\n" + body
    if not approved or tweet_id is not None:
        print('Post was not approved or already tweeted')
        return 200
    else:
        print(f" Approved post {approved} {tweet}  Tweet TBD {tweet_id} ")
        x = post_tweet(tweet)
        tweet_id = x['data']['id']
        update_post_tweet_status_code = update_post_tweet(doc_id, tweet_id)
        print(f"Posting to X {tweet}  {tweet_id}  {update_post_tweet_status_code}")
        return update_post_tweet_status_code