import requests
import json

def insert_document(project_id, dataset, token, document):
    """
    Inserts a new document into the Sanity Content Lake.

    Args:
    - project_id: Your Sanity project ID.
    - dataset: The dataset name (e.g., 'production').
    - token: The Sanity API token with write permissions.
    - document: The document to insert (should be a dictionary).

    Returns:
    - Response from the Sanity API.
    """
    # Construct the Sanity API endpoint
    url = f"https://{project_id}.api.sanity.io/v2021-06-07/data/mutate/{dataset}"

    # Set up the headers, including the Bearer token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Wrap the document in the appropriate payload format
    payload = {
        "mutations": [
            {
                "create": document
            }
        ]
    }

    # Make the POST request to insert the document
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the insertion was successful
    if response.status_code == 200:
        print("Document inserted successfully!")
        return response.json()
    else:
        print(f"Failed to insert document: {response.status_code}")
        print(f"Error: {response.text}")
        return None

# Example usage
project_id = "rh2kgtdt"
dataset = "production"
token = "sklJepUmCSdZc5PUkQQr0gTQL0e3dN2kIapGB1bHykyTNrsXJz6V95Gj53woI2c54Gq5r7FTOQSaeGCzgNLBtBLKl2G2Ycz23zlmz6OEFcME8rZRuqCByvZIHtIP30kSIQxPaSsmfzmRijKBSAZUoKuTZNrNWXRj4MeDJxMMeNG8kIAEDwkR"

# Define a new document to insert
document = {
    "_type": "post",
    "header": "test post 45",
    "body":[
        {
            "_type": "block",
            "_key": "43",
            "children": [
                {
                    "_type": "span",
                    "text": "This is the content of the blog post 45.",
                }
            ]
        }
      ],
    "date": "2024-10-01 16:36",
    "cta": "https://dannylieberman.com/waitlist"
    }

# Insert the document into the Sanity Content Lake
insert_document(project_id, dataset, token, document)

