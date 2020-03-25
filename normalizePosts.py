import re 
import pandas as pd
import nltk
import spacy

import inflect

from contractions import CONTRACTION_MAP
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')

# the following words might be useful to keep for the purpose of sentiment classification
# i.e. 'no' or 'not' could indicate negative sentiment 
words_list_keep = ["no", "not", "shoudn't", "couldn't", "aren't", "didn't"]

def change_stopwords(words_list = words_list_keep):
	for word in words_list:
		try:
			stopword_list.remove(word) 
			print(word, 'removed')
		except:
			continue

change_stopwords(words_list_keep)

# import training data
input_file = 'raw_train_df.csv'

train_df = pd.read_csv(input_file, encoding='utf-8')
train_df = train_df.fillna('')
train_df['shared_text'] = train_df['shared_text'].apply(lambda x: x.split('\n', 1)[-1])

# other functionalities:
# n-gram tagging so that proper nouns stay together

# this function removes various types of left/right quote marks
# and also replaces single left/right quote marks with regular ones
def fix_quotes(text):
	pattern = r'["“”„”«»]'
	text = re.sub(pattern, '', text)
	pattern = r'[‛’]'
	text = re.sub(pattern, '\'', text)
	return text

# NOTE: this does not work for contractions inside quotations
def expand_contractions(words, contraction_mapping=CONTRACTION_MAP):
	contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
		flags=re.IGNORECASE|re.DOTALL)

	def expand_match(contraction):
		match = contraction.group(0)
		first_char = match[0]
		expanded_contraction = contraction_mapping.get(match)\
		if contraction_mapping.get(match)\
		else contraction_mapping.get(match.lower())                       
		expanded_contraction = first_char+expanded_contraction[1:]
		return expanded_contraction

	expanded_text = contractions_pattern.sub(expand_match, words)
	expanded_text = re.sub("'", "", expanded_text)
	return expanded_text

# perhaps we can perform a count of exclams '!' separately

# gets rid of punctuation (i.e. '.', '!', '?')
def remove_special_characters(text, remove_digits=False):
	pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
	text = re.sub(pattern, '', text)
	return text

# removes short words of little use (e.g. 'and', 'the'...)
def remove_stopwords(words, is_lower_case=False):
	tokens = tokenizer.tokenize(words)
	tokens = [token.strip() for token in tokens]
	if is_lower_case:
		filtered_tokens = [token for token in tokens if token not in stopword_list]
	else:
		filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
	filtered_words = ' '.join(filtered_tokens)    
	return filtered_words

# we use the inflect library to replace numbers with textual representations 
# (way easier than my hand-made dictionary!)
def replace_numbers(words):
	p = inflect.engine()
	new_words = []
	for word in words:
		if word.isdigit():
			new_word = p.number_to_words(word)
			new_words.append(new_word)
		else:
			new_words.append(word)
	return new_words

# NOTE: convert numbers to text before proceeding with this step? 
# we lemmatize nouns, verbs, adjectives
def lemmatize(words):
	lemmatizer = WordNetLemmatizer()
	lemmatized_words = []
	for word, tag in pos_tag(words):
		if tag.startswith('NN'):
			pos = 'n'
		elif tag.startswith('VB'):
			pos = 'v'
		else:
			pos = 'a'
		lemmatized_words.append(lemmatizer.lemmatize(word, pos))
	return lemmatized_words

# needed to lemmatize the first element of the word tuple (string, POS)
# may want to adjust lemmatization depending on POS (noun, verb, adjective)
def lemmatize(words):
	lemmatizer = WordNetLemmatizer()
	lemmatized_words = []
	for word in words:
		lemma = lemmatizer.lemmatize(word[0])
		lemmatized_words.append(lemma)
	return lemmatized_words

## normalizing steps:

# combine post text and shared text fields
train_df.insert(0, 'text', train_df['post_text'] + ' ' + train_df['shared_text'])
train_df = train_df.drop(columns = ['post_text', 'shared_text'])

# drop rows where the number of shares is 0: this is a bug in facebook_scraper
train_df = train_df[train_df['shares'] != 0]
train_df = train_df.reset_index(drop = True)

# dummify image field: 1 if there was an image, 0 if there wasn't
train_df['image'] = train_df['image'].apply(lambda x: 0 if x == '' else 1)

# print('raw expression', train_df.text[139])
# normalize text: remove quotes THEN expand contractions, remove special characters and stopwords
train_df['text'] = train_df['text'].apply(lambda x: fix_quotes(x))
print('after removing quotes...')
# test = train_df.text[139]
train_df['text'] = train_df['text'].apply(lambda x: expand_contractions(x))
print('after expanding contractions...')
train_df['text'] = train_df['text'].apply(lambda x: remove_special_characters(x))
print('removing special characters...')

# train_df['text'] = train_df['text'].apply(lambda x: remove_stopwords(x))
# print('after removing stop words...', train_df.text[139])

# tokenize by splitting each sentence before lemmatizing 
# train_df['text'] = train_df['text'].apply(lambda x: pos_tag(x.split()))
# print('tokenizing sentences and tagging...', train_df.text[10])
# train_df['text'] = train_df['text'].apply(lambda x: lemmatize(x))
# print('after lemmatizing...', train_df.text[139])

train_df.to_csv('normalized_train_df.csv', index = False, encoding='utf-8')