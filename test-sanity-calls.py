from bl_sanity_utils import update_post_tweet, select_all, get_id_by_header


data=select_all("post")
# Iterate through the list of dictionaries
print(data)



"""# Example usage: Update a document with a specific tweet_id
document_id = "7rjsYFdOXTENOIKaMfUvnk"
#1844254612678713698
generated_tweet_id = 1843601879114076199
res = update_post_tweet(document_id, generated_tweet_id)
print(res)
"""
# Test case: get a  document _id by header
post_header = 'The first thing you do after selling a startup?'
post_id = get_id_by_header(post_header)
print(post_id)

generated_tweet_id = '1843601879114076199'
res = update_post_tweet(post_id, generated_tweet_id)
print(res)