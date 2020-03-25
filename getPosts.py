import pandas as pd
from facebook_scraper import get_posts

# Groups:
# Wild Green Memes 
# group_id = '1939160426313198'

# birb (O v O)
# group_id = '1024490957622648'

# Pages:
# another bird page 
# Another-Birb-Page-189872135059744

# Birb memes
# BirbMemesOfficial 

# National Geographic
# natgeo

## we will keep the text, the image to determine whether the post contained an image or not
## and we will keep likes, comments, and shares to gauge popularity 

def build_train_data(num_pages):
	# each post is in the form of a dict
	for index, post in enumerate(get_posts('natgeo', pages = num_pages, sleep = 5)):
		if index == 0:
			print('creating training data... ')
			train_df = pd.DataFrame(post, index = [0])
		else:
			train_df = train_df.append(pd.DataFrame(post, index = [0]), ignore_index = True)
	return train_df[['post_text', 'shared_text', 'image', 'likes', 'comments', 'shares']]

# the field 'text' = 'post_text' + 'shared_text'...
# ... but these fields need to be cleaned up first 

train_df = build_train_data(100)
train_df.to_csv('raw_train_df.csv', index = False, encoding='utf-8')