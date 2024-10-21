import requests
from dotenv import load_dotenv
import os
import urllib.parse
from bl_sanity_utils import *
# Load environment variables for global reference
load_dotenv()
project_id = os.getenv("SANITY_PROJECT_ID")
dataset = os.getenv("SANITY_DATASET")
token = os.getenv("SANITY_TOKEN")
api_version = os.getenv("SANITY_API_VERSION")


# Function to fetch document IDs
def fetch_document_ids(query):
    data = query_sanity_documents(query)
    print(data['result'])
    return data['result']

def remove_cta_field(document_ids):
    mutations = [{"patch": {"id": doc_id, "unset": ["cta"]}} for doc_id in document_ids]
    payload = {"mutations": mutations}
    sanity_mutate_url = f"https://{project_id}.api.sanity.io/{api_version}/data/mutate/{dataset}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(sanity_mutate_url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Successfully removed 'cta' from {len(document_ids)} documents.")
    else:
        print(f"Error removing 'cta' field: {response.status_code} {response.text}")

# Function to delete documents by ID
def delete_documents(document_ids):
    mutations = [{"delete": {"id": doc_id}} for doc_id in document_ids]
    payload = {
        "mutations": mutations
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    delete_url = f'https://{project_id}.api.sanity.io/v2021-06-07/data/mutate/{dataset}'
    response = requests.post(delete_url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Successfully deleted {len(document_ids)} documents.")
    else:
        print(f"Error deleting documents: {response.status_code} {response.text}")

# Main logic
#query = '*[_type == "post" && header match "*test*"]._id'
#query =  '*[_type == "post" && tweet_id  == null ]._id'
query =  '*[_type == "post"]._id'
print(query)
document_ids = fetch_document_ids(query)

if document_ids:
    print(f"Found {len(document_ids)} documents to remove CTA field.")
    #delete_documents(document_ids)
    remove_cta_field(document_ids)
else:
    print("No documents found.")
