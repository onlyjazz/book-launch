from dotenv import load_dotenv
from datetime import datetime

def bl_insert_sanity_document(post_header, post_content):
    import json
    import os
    from requests import post
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

    url = f"https://{project_id}.api.sanity.io/v2021-06-07/data/mutate/{dataset}"

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



# Insert the document into the Sanity Content Lake
llm_title = "Test 52 Fighting Biotech Burnout: Strategies for Sustainable Productivity"
llm_text = "**Set Clear Boundaries:** Establish defined working hours and stick to them. Avoid checking emails or work messages outside these hours to create a clear separation between work and personal life."
bl_insert_sanity_document(llm_title, llm_text)
