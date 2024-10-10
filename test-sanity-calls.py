from bl_sanity_utils import update_post_tweet, select_all
data=select_all("post")
# Iterate through the list of dictionaries
#print(data)
print('_id                                  '.ljust(50),'header'.ljust(10),     'Tweet Id')
print('-------------------------------------'.ljust(50,'-'), '---------', '---------')
for document in data:
    print(f"{(document['_id']).ljust(50)}  {document['header'][:8]}  {document['tweet_id']}")


# Example usage: Update a document with a specific tweet_id
document_id = "7rjsYFdOXTENOIKaMfUvnk"
#1844254612678713698
generated_tweet_id = 1843601879114076199
res = update_post_tweet(document_id, generated_tweet_id)
print(res)