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

## the following is a neat workaround for wrapping text in the hovertemplate! 
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

def create_scatter(score_type, figname, x_title, title, color = 'blue'):
	fig = go.Figure(data = go.Scatter(
		x = scored_df[score_type], 
		y = scored_df.shares,
		text = scored_df.text,
		hovertemplate = 'Facebook Post:<br>%{text}<br>' + 'Shares: %{y:.0f}<br>' + 'Score: %{x:.1f}' + '<extra></extra>',
		hoverinfo = 'text',
		mode = 'markers',
		marker = dict(color = color)
	))

	fig.update_layout(
		title = title,
		title_x = 0.5,
		xaxis_title = x_title,
		yaxis_title = "Number of Shares",
		autosize = True
	)
	# fig.show()
	upload_to_chart_studio(fig, figname)

# Box plot of shares separated by positive, neutral, negative score
def create_boxplot(score_type, lower_score, upper_score, title, figname):
	layout = go.Layout(yaxis=dict(range=[0, 6000]))
	fig = go.Figure(layout = layout)
	fig.add_trace(go.Box(y = scored_df.shares[scored_df[score_type] < lower_score], 
		name = 'Scores < ' + str(lower_score) + '<br>n = ' + str(scored_df.shares[scored_df.score < lower_score].count())))
	fig.add_trace(go.Box(y = scored_df.shares[scored_df[score_type].between(lower_score, upper_score)],
		name = str(lower_score) + ' ≤ Scores ≤ ' + str(upper_score) + '<br>n = ' 
		+ str(scored_df.shares[scored_df[score_type].between(lower_score, upper_score)].count())))
	fig.add_trace(go.Box(y = scored_df.shares[scored_df[score_type] > upper_score], 
		name = 'Scores > ' + str(upper_score) + '<br>n = ' + str(scored_df.shares[scored_df[score_type] > upper_score].count())))
	fig.update_layout(
		title = title,
		title_x = 0.5,
		yaxis_title = 'Number of Shares',
		showlegend = False
	)
	# fig.show()
	upload_to_chart_studio(fig, figname)

def create_violinplot(score_type, lower_score, upper_score):
	fig = go.Figure()
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score < lower_score], 
		name = 'Scores < ' + str(lower_score) + '<br>n = ' + str(scored_df.shares[scored_df.score < lower_score].count())))
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score.between(lower_score, upper_score)],
		name = str(lower_score) + ' ≤ Scores ≤ ' + str(upper_score) + '<br>n = ' 
		+ str(scored_df.shares[scored_df.score.between(lower_score, upper_score)].count())))
	fig.add_trace(go.Violin(y = scored_df.shares[scored_df.score > upper_score], 
		name = 'Scores >' + str(upper_score) + '<br>n = ' + str(scored_df.shares[scored_df.score > upper_score].count())))
	fig.update_layout(
		title = "Number of Shares vs. Sentiment Score for National Geographic Facebook Posts",
		title_x = 0.5,
		yaxis_title = 'Number of Shares',
		showlegend = False
	)
	# fig.show()
	upload_to_chart_studio(fig, 'violin_shares_by_score')

# other visualizations to consider:

# number of words in each post
# scored_df.text.apply(lambda x: len(x.split()))

create_scatter(score_type = 'score', 
	figname = 'sentiment_vs_score', 
	x_title = 'Sentiment Score',
	title = "Number of Shares vs. Sentiment Score for National Geographic Facebook Posts"
)
create_scatter(score_type = 'overall_score', 
	figname = 'sentiment_vs_overall_score', 
	x_title = 'Overall Score',
	title = "Number of Shares vs. Overall Score for National Geographic Facebook Posts", 
	color = 'green'
)
create_boxplot(score_type = 'score', lower_score = -1, upper_score = 1, 
	title = 'Number of Shares vs. Sentiment Score for National Geographic Facebook Posts', 
	figname = 'sentiment_score_boxplot'
)
create_boxplot(score_type = 'overall_score', lower_score = -1, upper_score = 1, 
	title = 'Number of Shares vs. Overall Score for National Geographic Facebook Posts',
	figname = 'overall_score_boxplot'
)
# create_violinplot(-1,1)
