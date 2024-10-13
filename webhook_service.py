from flask import Flask, request, jsonify
import json
from bl_sanity_utils import sanity_to_x
# Initialize Flask app
app = Flask(__name__)



# Define the webhook endpoint
@app.route('/sanity-webhook', methods=['POST'])
def handle_webhook():
    try:
        # Parse the incoming data
        content = request.get_json()
        # Log the incoming webhook data (optional)
        print("Webhook received - calling function sanity_to_x: ")
        print('-------------------------------------------------\n')
        pretty_json = json.dumps(content, indent=4)
        print(pretty_json)
        print('-------------------------------------------------\n')
        res=sanity_to_x(content)
        return jsonify({"status": res, "message": 'tweet processed'}), 200

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 404



# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
