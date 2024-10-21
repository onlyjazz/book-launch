from bl_sanity_utils import *
from bl_twitter_utils import *
# Test usage of post_tweet(content)
x = """
🔥My novel is now Pre-Order on Amazon!  

"Bob and Alice - An Anti-Love Story" is my first novel and third book.

I started writing "Bob and Alice" after I sold my clinical data management company, 7 months ago.

The novel was (and still is) many things for me.

The novel takes place in Venice, California, not far from my first job at Wilshire Associates.

Like any novel, it draws on people I've met and worked with.

The names and details have been changed.

I would not want someone waiting for me by my house with a pistol.

"Bob and Alice" is a therapeutic exercise to release me from the demons of my past.

It's a journey into the hearts of two high-performing people, each navigating the shadows of their own fears and the demands of their careers. 

The novel was a platform for me to learn how to write after I did the twitter writing course with @Tim_Denning

The writing process taught me that good writing starts with good reading - I've had the good fortune to read the collected short stories of Isaac Babel
and return to Hemingway and Kurt Vonnegut and read Virginia Wolff for the first time.

Bob, is a Silicon Valley CTO just fired from big tech in mid 2023.
 
Alice left 80 billable hours/week at a high-powered LA law firm for a 9-to-5 at the FBI field in LA.
 
She finds herself entangled in a web of international terror financing, personal challenges, and the unpredictable currents of her love story with Bob.

Between high-stakes, high-tech and intimate moments, Bob and Alice explores the profound truth that a relationship thrives when both man and woman share the load, trusting each other to stand strong in their own moments of vulnerability.
"""

#post_response = post_tweet(x)
# Extract the ID
#tweet_id = post_response['data']['id']


# get tweet_id by post header for testing
#header='How Do You Navigate Financing Pressures in a Seed-Stage Tech Startup?'
#post = get_post_by_header(header)
#tweet_id = post['tweet_id']
#print(f"Extracted Twitter ID: {tweet_id}")
#print(tweet_id)
#metrics = get_tweet_metrics(tweet_id)
#if metrics:
#    print(f"Engagement_rate: {metrics['engagement_rate']}")
#    print(f"Impressions: {metrics['impression_count']}")
#else:
#    print("Failed to retrieve tweet metrics.")

# loop on posts
#query = '*[_type == "post"] | order(header asc) { _id, tweet_id, header }'
query = '*[_type == "post" && !(_id in path("drafts.**"))] | order(header asc) { _id, tweet_id, header }'

document_ids  = query_sanity_documents(query)
#print(document_ids['result'])
print('Query returned ', len(document_ids['result']), 'published posts')
i=0
for post in document_ids['result']:
    i+=1
    doc_id = post['_id']
    tweet_id = post['tweet_id']
    #metrics = get_tweet_metrics(tweet_id)
    #engagement_rate = metrics['engagement_rate']
    #impression_count = metrics['impression_count']
    header = post['header']
    print(
        f'{i} header {header}, tweet_id {tweet_id}, doc_id {doc_id}')

