import pandas as pd

from afinn import Afinn
from textblob import TextBlob

# import normalized training data
input_file = './data/normalized_df.csv'
output_file = './data/scored_df.csv'

normalized_train_df = pd.read_csv(input_file, encoding='utf-8')

# the model is a bit simplistic: perhaps animals/nature terms should be considered positive scoring?

def get_sentiment_scores(train_df):
	train_df.insert(0, 'score', value = 0)
	train_df['score'] = train_df['text'].apply(lambda x: Afinn().score(x))
	return train_df

scored_train_df = get_sentiment_scores(normalized_train_df)
scored_train_df.to_csv(output_file, index = False, encoding='utf-8')