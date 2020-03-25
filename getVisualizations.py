import pandas as pd
import plotly.graph_objects as go

input_file = './data/scored_df.csv'

scored_df = pd.read_csv(input_file, encoding='utf-8')

def create_scatter():
	return 0

fig = go.Figure(data = go.Scatter(
	x = scored_df.score, 
	y = scored_df.shares,
	hovertext = scored_df.text,  
	mode = 'markers'))

fig.update_layout(
	title="Popularity vs. Sentiment for National Geographic Facebook Posts ",
	xaxis_title="Sentiment Score [number of positive words]",
	yaxis_title="Number of Shares"
)

fig.show()

# number of words in each post
# scored_df.text.apply(lambda x: len(x.split()))