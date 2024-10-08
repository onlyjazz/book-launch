from bl_twitter_utils import post_tweet, get_tweet_metrics
# Test usage of post_tweet(content)
x = """
🔥My novel is now Pre-Order on Amazon!  

"Bob and Alice - An Anti-Love Story" is a thrilling journey into the hearts of two high-performing individuals, each navigating the shadows of their own fears and the demands of their careers. Bob, a Silicon Valley CTO, and Alice, a fiercely dedicated FBI lawyer, find themselves entangled in a web of international intrigue, personal challenges, and the unpredictable currents of love.

Between high-stakes missions and intimate moments, Bob and Alice explores the profound truth that a relationship thrives when both man and woman share the load, trusting each other to stand strong in their own moments of vulnerability.
"""

post_response = post_tweet(x)
# Extract the ID
tweet_id = post_response['data']['id']

# Print the ID
print(f"Extracted Twitter ID: {tweet_id}")

metrics = get_tweet_metrics(tweet_id)
if metrics:
    print(f"Likes: {metrics['like_count']}")
    print(f"Impressions: {metrics['impression_count']}")
else:
    print("Failed to retrieve tweet metrics.")

