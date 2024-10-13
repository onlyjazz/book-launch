from flask import Flask, request, jsonify
import json
from bl_twitter_utils import post_tweet
from bl_sanity_utils import update_post_tweet
# Initialize Flask app
app = Flask(__name__)

def post_to_x(content: object) -> object:
    # Parse the incoming Sanity document
    doc_id= content["_id"]
    header = content['header']
    body = content['body'][0]['children'][0]['text']
    #tweet = header + "\n\n" + body
    print(f" {doc_id} {header}   {body}")
    """
    # Post to X and return the tweet_id
    x = post_tweet(tweet)
    tweet_id = x['data']['id']
    # Update the Sanity document with the tweet_id
    update_post_tweet_status_code = update_post_tweet(doc_id, tweet_id)
    print(f"Posting to X {tweet}  {tweet_id}  {update_post_tweet_status_code}")
    """

    return "Posted to X"

# Define the webhook endpoint
@app.route('/sanity-webhook', methods=['POST'])
def handle_webhook():
    try:
        # Parse the incoming data
        content = request.get_json()

        # Log the incoming webhook data (optional)
        print("Webhook received: ")
        res=post_to_x(content)
        return jsonify({"status": res, "message": 'tweet processed'}), 200

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
