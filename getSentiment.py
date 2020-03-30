import pandas as pd
import pickle

from afinn import Afinn
from textblob import TextBlob

# import normalized training data
input_file = './data/normalized_df.csv'
output_file = './data/scored_df.csv'
dict_input_file = './dictionaries/animal_dict.pickle'

normalized_train_df = pd.read_csv(input_file, encoding='utf-8')

# Load animal score dictionary
with open(dict_input_file, 'rb') as handle:
    animal_dict = pickle.load(handle)

# any animal terms for neutral/positive scores get a slight positive bump
# the mention of animals for negative scores don't have an impact
# this is to ensure a negative phrase like, 'I hate kittens' doesn't get a positive bump

def get_sentiment_scores(train_df):
	train_df.insert(0, 'score', value = 0)
	train_df['score'] = train_df['text'].apply(lambda x: Afinn().score(x))
	return train_df

# this function returns the animal score whenever checking an animal in the Facebook post text 
# negative posts with animal mentions become more negative
def get_animal_score(animal, x):
	if animal.lower() in x['text'].lower() and x['score'] >= 0:
		# print('found', animal.lower(), 'in positive text:', '"', x['text'], '"')
		return animal_dict[animal]
	elif animal.lower() in x['text'].lower() and x['score'] < 0:
		# print('found', animal.lower(), 'in negative text:', '"', x['text'], '"')
		# print('adding score:', -1*animal_dict[animal], 'to sentiment score')
		return -1.0*animal_dict[animal]
	else:
		# print('did not find anything in text')
		return 0

def get_overall_scores(train_df):
	train_df.insert(0, 'animal_score', value = 0)
	# add an animal score if animals are present in a Facebook Post
	for animal in animal_dict.keys():
		train_df['animal_score'] += train_df.apply(lambda x: get_animal_score(animal, x), axis = 1)
	train_df.insert(0, 'overall_score', value = train_df['score'] + train_df['animal_score'])
	return train_df

scored_train_df = get_sentiment_scores(normalized_train_df)
scored_train_df = get_overall_scores(scored_train_df)
scored_train_df.to_csv(output_file, index = False, encoding='utf-8')