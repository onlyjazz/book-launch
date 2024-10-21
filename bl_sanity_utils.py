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

def update_post_statistics(doc_id, engagement_rate, impression_count):
    """
        Update a single post with tweet statistics for the post
        :param doc_id:
        :param engagement_rate:
        :param impression_count:
        :return: 200 or failure and log_response
    """
    mutation = {
        "mutations": [
            {
                "patch": {
                    "id": doc_id,
                    "set": {
                        "engagement_rate": engagement_rate,
                        "impression_count": impression_count
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
    log_query_response(' "patch": {"id": doc_id,"set": {"impression_count": impression_count, "engagement_rate": engagement_rate }', response)
    return response.status_code


def update_prompt_stats(doc_id, impression_count, engagement_rate):
    """
        Update a single prompt with tweet statistics for the prompt
        :param doc_id:
        :param impression_count
        :param engagement_rate:
        :return: 200 or failure and log_response
    """
    mutation = {
        "mutations": [
            {
                "patch": {
                    "id": doc_id,
                    "set": {
                        "impression_count": impression_count,
                        "engagement_rate": engagement_rate
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
    log_query_response(' "patch": {"id": doc_id,"set": {"impression_count": impression_count, "engagement_rate": engagement_rate}', response)
    return response.status_code

def update_post_tweet(doc_id, tweet_id):
    """
        Update a single post with tweet_id
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
    cta = get_cta()
    post_content_cta = post_content + "\n\n" + cta
    url = f"https://{project_id}.api.sanity.io/{api_version}/data/mutate/{dataset}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    doc = {
        "_type": "post",
        "header": post_header,
        "cta": get_cta(),
        "draft": [
            {
                "_type": "block",
                "_key": "1",
                "children": [
                    {
                        "_type": "span",
                        "text": post_content_cta,
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
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
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

def get_system_prompt(current_cycle):
    # Query prompt. Body is portable text field, return a string
    query = f'*[_type == "prompt" && cycle == {current_cycle}]{{"body": pt::text(body)}}'
    data = query_sanity_documents(query)
    p = data['result'][0]['body']
    return p

def get_cta():
    current_cycle = get_cycle()
    query = f'*[_type == "prompt" && cycle == {current_cycle}]{{cta}}'
    data = query_sanity_documents(query)
    p = data['result'][0]
    return p['cta']

def get_id_by_header(header):
    # Query prompt documents by dow, body is portable text field, return a string
    query = f'*[_type == "post" && header == "{header}"]'
    data = query_sanity_documents(query)
    return data['result'][0]['_id']

def get_prompt_id_by_identifier(identifier):
    query = f'*[_type == "prompt" && identifier == "{identifier}"]._id'
    data = query_sanity_documents(query)
    return data['result'][0]

def get_post_by_header(header):
    # Query prompt documents by header
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

def max_cycle():
    """
        Query the cycle data type and return the max value of the cycle
        :param
        :return:
        max value or failure and log_response
    """
    query = f'math::max(*[_type == "prompt"].cycle)'
    data = query_sanity_documents(query)
    return data['result']


def set_cycle():
    """
        Increment and update the round of the publishing cycle
        :return: 200 or failure and log_response
    """
    # Query the cycle record
    query = f'*[_type == "cycle"]'
    data = query_sanity_documents(query)
    doc_id = data['result'][0]['_id']
    # increment modulo number of prompts in the database
    mc = max_cycle()
    m = data['result'][0]['round']
    m += 1
    n = m % mc
    if n == 0:
        n = mc
    mutation = {
        "mutations": [
            {
                "patch": {
                    "id": doc_id,
                    "set": {
                        "round": n
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
    groq_query_string = f'"patch": {{"id": {doc_id}, "set": {{"round": {n}}}}}'
    log_query_response(groq_query_string, response)
    return response.status_code


def get_cycle():
    # Get the latest round of the publishing cycle
    query = f'*[_type == "cycle"]{{round}}'
    data = query_sanity_documents(query)
    return data['result'][0]['round']