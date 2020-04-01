import pandas as pd 
import requests
import re
# for saving the animal to score dictionary
import pickle

from bs4 import BeautifulSoup

animal_page = 'https://a-z-animals.com/animals/'
page_response = requests.get(animal_page, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")

# all of the animals listed are in 'bold' tags which makes them convenient to extract
animal_content = page_content.find_all('b')
animal_list = [s.text for s in animal_content]

# there are a few phrases also in bold tags at the beginning which we ignore
# we start after the bold text, 'Jump to letter' on the webpage
# this is sort of a hacky solution though... perhaps using div tags is better
animal_list = animal_list[6:]

# we pluralize a list of words with some basic rules
def pluralize_list(singular_list):
	plurals_list = []
	for word in singular_list:
		# words ending in 'o' sometimes end in 'os' or 'oes' so we include them both
		if any(word.endswith(suffix) for suffix in ['o']):
			plurals_list.append(word + 's')
			plurals_list.append(word + 'es')
		# account for word that need 'es' to be pluralized
		elif any(word.endswith(suffix) for suffix in ['sh', 'ch', 'z', 's', 'x', 'j']):
			plurals_list.append(word + 'es')
		# bunny --> bunnies: remove 'y' and replaces with 'ies' 
		elif any(word.endswith(suffix) for suffix in ['y']):
			plurals_list.append(word[:-1] + 'ies')
		# wolf --> wolves: remove 'f' and replace with 'ves'
		elif any(word.endswith(suffix) for suffix in ['f']):
			plurals_list.append(word[:-1] + 'ves')
		else:
			plurals_list.append(word + 's')
	return singular_list.extend(plurals_list)

pluralize_list(animal_list)
# assign each animal a score of 2.0 (on a scale of 1.0-5.0)
animal_dict = {key: 1.0 for key in animal_list}

# Store data in HIGHEST_PROTOCOL smallest format
with open('./dictionaries/animal_dict.pickle', 'wb') as handle:
	pickle.dump(animal_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


