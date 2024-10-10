from sys import sanity_api_version

from dotenv import load_dotenv
from datetime import datetime
import json

from openai import base_url
from requests import post
import os
import requests


# Load environment variables for global reference
load_dotenv()
project_id = os.getenv("SANITY_PROJECT_ID")
dataset = os.getenv("SANITY_DATASET")
token = os.getenv("SANITY_TOKEN")
sanity_api_version = os.getenv("SANITY_API_VERSION")

# Function to update a document with the generated tweet_id
def update_post_tweet(doc_id, tweet_id):
    # Define the mutation to update the document with the new tweet_id
    #groq_query = f'*[_type == "post" && _id == "{doc_id}"]' didn't work
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

    # Set up the headers, including the Bearer token for authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # Make the POST request to apply the mutation
    url = f"https://{project_id}.api.sanity.io/{sanity_api_version}/data/mutate/{dataset}"
    response = requests.post(url, json=mutation, headers=headers)

    # Check if the mutation was successful
    if response.status_code == 200:
        print(f"Post {doc_id} updated successfully with tweet_id: {tweet_id}")
        return response.json()
    else:
        print(f"Failed to update Post: {response.status_code}")
        print(f"Error: {response.text}")
        return None


def insert_post(post_header, post_content):
    """
    Inserts a new post document into the Sanity Content Lake.

    Args:
    - document: The document to insert (should be a dictionary).

    Returns:
    - Response from the Sanity API.
    """

    url = f"https://{project_id}.api.sanity.io/v2024-10-05/data/mutate/{dataset}"

    # Set up the headers, including the Bearer token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    # Construct the JSON doc from the function arguments
    # post_content stored in a portable text field and a markdown field
    # Get the current timestamp and format it as "YYYY-MM-DD HH:MM"
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
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
        "date": current_timestamp,
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

    # Check if the insertion was successful
    if response.status_code == 200:
        print("Document inserted successfully!")
        return response.json()
    else:
        print(f"Failed to insert document: {response.status_code}")
        print(f"Error: {response.text}")
        return None


def query_sanity_documents(groq_query):
    # Construct the Sanity API endpoint
    # Read the environment variables
    load_dotenv()
    project_id = os.getenv("SANITY_PROJECT_ID")
    dataset = os.getenv("SANITY_DATASET")
    token = os.getenv("SANITY_TOKEN")
    url = f"https://{project_id}.api.sanity.io/v2024-10-05/data/query/{dataset}"

    # Set up the headers, including the Bearer token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, params={"query": groq_query}, headers=headers)
    # Check if the query was successful
    if response.status_code == 200:
        log_query_response(groq_query, response)
        return response.json()
    else:
        print(f"Failed to query document: {response.status_code}")
        print(f"Error: {response.text}")
        return None


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

def select_all(dataType):
    # Select _id and header fom dataType no WHERE clause
    query = f'*[_type == "{dataType}"] | order(_createdAt desc)[0..1000]{{_id, header, tweet_id}}'
    data = query_sanity_documents(query)
    return  data['result']
