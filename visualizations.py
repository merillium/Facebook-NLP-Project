import pandas as pd
import plotly.graph_objects as go

input_file = 'scored_train_df.csv'

scored_df = pd.read_csv(input_file, encoding='utf-8')

def create_scatter():
	return 0

fig = go.Figure(data = go.Scatter(x = scored_df.scores, y = scored_df.shares, mode = 'markers'))
fig.show()