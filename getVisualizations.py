import pandas as pd
import plotly.graph_objects as go

import chart_studio
import chart_studio.plotly as ch_py
import chart_studio.tools as tls

input_file = './data/scored_df.csv'

## NOTE: anyone using this will need to make their own text file: 
# 'chart_studio_info.txt' saved in the highest directory
# username goes on line 1, API key goes on line 2
user_info_file = 'chart_studio_info.txt'

scored_df = pd.read_csv(input_file, encoding='utf-8')

## the following is a work around for wrapping text in the hovertemplate
scored_df.text = scored_df.text.str.wrap(30)
scored_df.text = scored_df.text.apply(lambda x: x.replace('\n', '<br>'))

def upload_to_chart_studio(fig, filename):
	# push to chart_studio account
	# regenerate api key if necessary

	# private information stored locally:
	f = open(user_info_file, 'r')
	userinfo = f.read().split()
	f.close()
	username, api_key = userinfo 

	chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
	ch_py.plot(fig, filename = filename, auto_open = True)

def create_scatter():
	fig = go.Figure(data = go.Scatter(
		x = scored_df.score, 
		y = scored_df.shares,
		text = scored_df.text,
		hovertemplate = 'Facebook Post:<br>%{text}<br>' + 'Shares: %{y:.0f}<br>' + 'Score: %{x:.1f}' + '<extra></extra>',
		hoverinfo = 'text',
		mode = 'markers')
	)

	fig.update_layout(
		title="Popularity vs. Sentiment Score for National Geographic Facebook Posts",
		title_x = 0.5,
		xaxis_title="Sentiment Score",
		yaxis_title="Number of Shares",
		autosize = True
	)
	# fig.show()
	upload_to_chart_studio(fig, 'score_vs_popularity')

# Box plot of shares separated by positive, neutral, negative score
def create_boxplot(lower_score, upper_score):
	fig = go.Figure()
	fig.add_trace(go.Box(y = scored_df.shares[scored_df.score < lower_score], 
		name = 'Scores < ' + str(lower_score) + '<br>n = ' + str(scored_df.shares[scored_df.score < lower_score].count())))
	fig.add_trace(go.Box(y = scored_df.shares[scored_df.score.between(lower_score, upper_score)],
		name = str(lower_score) + ' < Scores < ' + str(upper_score) + '<br>n = ' 
		+ str(scored_df.shares[scored_df.score.between(lower_score, upper_score)].count())))
	fig.add_trace(go.Box(y = scored_df.shares[scored_df.score > upper_score], 
		name = 'Scores > ' + str(upper_score) + '<br>n = ' + str(scored_df.shares[scored_df.score > upper_score].count())))
	fig.update_layout(
		yaxis_title = 'Number of Shares',
		showlegend = False
	)
	# fig.show()
	# upload_to_chart_studio(fig, 'score_vs_popularity')

def create_violinplot(lower_score, upper_score):
	fig = go.Figure()
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score < lower_score], 
		name = 'Scores < ' + str(lower_score) + '<br>n = ' + str(scored_df.shares[scored_df.score < lower_score].count())))
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score.between(lower_score, upper_score)],
		name = str(lower_score) + ' < Scores < ' + str(upper_score) + '<br>n = ' 
		+ str(scored_df.shares[scored_df.score.between(lower_score, upper_score)].count())))
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score > upper_score], 
		name = 'Scores >' + str(upper_score) + '<br>n = ' + str(scored_df.shares[scored_df.score > upper_score].count())))
	fig.update_layout(
		yaxis_title = 'Number of Shares',
		showlegend = False
	)
	fig.show()
	# upload_to_chart_studio(fig, 'score_vs_popularity')

# other visualizations to consider:

# number of words in each post
# scored_df.text.apply(lambda x: len(x.split()))

# create_scatter()
# create_boxplot(-1,1)
# create_violinplot(-1,1)


