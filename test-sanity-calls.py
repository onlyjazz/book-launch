from bl_sanity_utils import update_post_tweet, select_all, get_id_by_header, get_system_prompt

# Test cases
data=select_all("prompt")
print(data)
for document in data:
    print(f"{(document['_id']).ljust(50)}  {document['header'][:18]}  {document['tweet_id']}")

post_header = 'The first thing you do after selling a startup?'
post_id = get_id_by_header(post_header)
print(post_id)

generated_tweet_id = '1843601879114076199'
res = update_post_tweet(post_id, generated_tweet_id)
print(res)

p = get_system_prompt()
print(p)