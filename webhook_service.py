from flask import Flask, request, jsonify
import json

# Initialize Flask app
app = Flask(__name__)


# Define your functions here
def read_from_sanity():
    # Your function to read data from Sanity
    print("Reading from Sanity...")
    return "Sanity data"


def post_to_x(content):
    # Your function to post to X
    print(f"Posting to X: {content}")
    return "Posted to X"


def extract_x_tweet_stats(tweet_id):
    # Your function to extract X stats
    print(f"Extracting stats for tweet ID: {tweet_id}")
    return {"likes": 10, "retweets": 5}


# Define the webhook endpoint
@app.route('/sanity-webhook', methods=['POST'])
def handle_webhook():
    try:
        # Parse the incoming data
        data = request.get_json()

        # Log the incoming webhook data (optional)
        print("Webhook received: ", json.dumps(data, indent=4))

        # Perform actions based on the webhook data
        if "trigger" in data:
            # Example action based on a specific field in your webhook payload
            if data["trigger"] == "read_sanity":
                result = read_from_sanity()
            elif data["trigger"] == "post_x":
                content = data.get("content", "Default content")
                result = post_to_x(content)
            elif data["trigger"] == "extract_x_stats":
                tweet_id = data.get("tweet_id")
                result = extract_x_tweet_stats(tweet_id)
            else:
                result = "Unknown trigger action"

        return jsonify({"status": "success", "result": result}), 200

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
