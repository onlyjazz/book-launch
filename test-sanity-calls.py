from bl_sanity_utils import *

# Test cases
#data=select_all("post")
#print(data)
#for document in data:
#    print(f"{(document['_id']).ljust(50)}  {document['header'][:18]}  {document['tweet_id']}")

#post_header = 'The first thing you do after selling a startup?'
#post_id = get_id_by_header(post_header)
#print(post_id)

#generated_tweet_id = '1843601879114076199'
#res = update_post_tweet(post_id, generated_tweet_id)
#print(res)

#p = get_system_prompt()
#print(p)

#post_header = 'Is late night shopping a solution for loneliness?'
#post_content= get_post_by_header(post_header)
#if post_content is None:
#    print(f"Post header {post_header} was  not found")
#else:
#    print(post_content['_id'] )
#    print(post_content['header'])
#    print(post_content['approved'])
#    print(post_content['body'])
#    print(post_content['tweet_id'])
#    sanity_to_x(post_content)


#print(get_cta())

#print(get_system_prompt())

#m = get_cycle()
#print(f'Current round {m}')
#system_prompt = get_system_prompt(m)
#print(system_prompt)
#print('\n-------------------------------------------------------------\n')

#set_cycle()
#next_cycle = get_cycle()
#print(f'Next round will be {next_cycle}')

#current_cycle = get_cycle()
#print('This round is:', current_cycle)
#cta = get_cta()
#print(cta)
#post_content = "abc" + cta
#print (post_content)

feedback_agent_post_stats()
feedback_agent_prompt_stats()

