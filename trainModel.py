import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score, precision_score

from sklearn.metrics import f1_score

input_file = './data/scored_df.csv'

# train model on data
df = pd.read_csv(input_file, encoding='utf-8')[['overall_score', 'animal_score', 'score', 'text', 'shares']]

# create a dummy variable from a threshold number of shares
# this isn't necessary as a decision tree tries these splits anyways
def categorize_score(x, lower_score, upper_score):
	if x < lower_score:
		return -1
	elif x > upper_score:
		return 1
	else:
		return 0

def create_dummy_shares(x, thresh_shares):
	if x > thresh_shares:
		return 1
	else:
		return 0

best_precision = 0.5 
list_num_shares = np.linspace(300,700,40)
for thresh_shares in list_num_shares:
	df['dummy_shares'] = df['shares'].apply(lambda x: create_dummy_shares(x, thresh_shares))

	features_df = df[['overall_score', 'animal_score', 'score']]
	target_df = df['dummy_shares']
	X_train, X_test, y_train, y_test = train_test_split(features_df, target_df, test_size = 0.8, random_state = 420)

	print('y_test imbalance:', sum(y_test == 1), 'out of', len(y_test))
	decision_tree = DecisionTreeClassifier(random_state=42, max_depth=4)
	decision_tree = decision_tree.fit(np.array(X_train), y_train)

	y_pred = decision_tree.predict(np.array(X_test))
	test_precision = precision_score(y_test, y_pred)
	if test_precision > best_precision:
		best_precision = test_precision
	print('Predicted facebook posts have less or more than', thresh_shares, 
		'shares with an precision of', test_precision)



