from dotenv import load_dotenv
from datetime import datetime
import json

from openai import base_url
from requests import post, Response
import os
import requests


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

    url = f"https://{project_id}.api.sanity.io/v2024-10-05/data/mutate/{dataset}"
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
        "cta": "https://dannylieberman.com/waitlist"
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
    return {response.status_code}


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

def select_all(dataType):
    # Select _id and header fom dataType no WHERE clause
    query = f'*[_type == "{dataType}"]{{_id, header, tweet_id}}'
    data = query_sanity_documents(query)
    return  data
