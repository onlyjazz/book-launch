import requests
# code snippets for improving / refactoring

# improve the query_sanity_documents
def execute_groq_query(query):
    url = 'your_sanity_api_endpoint'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your_token'
    }

    response = requests.get(url, params={'query': query}, headers=headers)

    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    else:
        return {"status": "error", "code": response.status_code}

def process_groq_result(result):
    if isinstance(result, list):
        print("Query successful! Retrieved posts:")
        for post in result:
            print(f"Post ID: {post['_id']}, Tweet ID: {post['tweet_id']}, Header: {post['header']}")
    elif isinstance(result, dict):
        print("Query successful but returned unexpected structure.")
        print(result)
    else:
        print(f"Error occurred. Status code: {result}")

# Example GROQ query with a projection
query = '*[_type == "post"]{_id, tweet_id, header}'

# Call the execute_groq_query function
result = execute_groq_query(query)

# Process the result using the helper function
process_groq_result(result)
