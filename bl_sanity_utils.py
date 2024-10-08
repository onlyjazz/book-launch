from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os
from requests import post


def insert_sanity_document(post_header, post_content):
    """
    Inserts a new document into the Sanity Content Lake.

    Args:
    - document: The document to insert (should be a dictionary).

    Returns:
    - Response from the Sanity API.
    """
    # Construct the Sanity API endpoint
    # Read the environment variables
    load_dotenv()
    project_id = os.getenv("SANITY_PROJECT_ID")
    dataset = os.getenv("SANITY_DATASET")
    token = os.getenv("SANITY_TOKEN")

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
        "markdown_body": post_content,
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
    response = requests.get(url, params={"query": groq_query})

    # Check if the query was successful
    if response.status_code == 200:
        print("Document queried successfully!")
        return response.json()
    else:
        print(f"Failed to query document: {response.status_code}")
        print(f"Error: {response.text}")
        return None


def get_system_prompt():
    current_date = datetime.now()
    current_dow = current_date.isoweekday()
    # Query prompt documents by dow, body is portable text field, return a string
    query = f'*[_type == "prompt" && dow == {current_dow}]{{"body": pt::text(body)}}'
    data = query_sanity_documents(query)
    p = data['result'][0]['body']
    return p
