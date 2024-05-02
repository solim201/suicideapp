import feedparser
import os
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import dash
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
from dash import dcc,html
import dash_mantine_components as dmc
from dash.dependencies import Input,Output
import numpy as np
from PIL import Image

subreddits=['all_together','depression_help','mentalhealth','SuicideBereavement','SuicideWatch'] 

app = dash.Dash(__name__)

def filter_data(all_merged, sub_list):
    filtered_df = all_merged[all_merged['forum'].isin(sub_list)]
    return filtered_df

os.chdir(os.path.dirname(os.path.abspath(__file__)))
all_merged = pd.concat([
    pd.read_csv('./data/new_post_depression_help_240420.csv', sep=";"),
    pd.read_csv('./data/new_post_mentalhealth_240420.csv', sep=";"),
    pd.read_csv('./data/new_post_SuicideBereavement_240420.csv', sep=";"),
    pd.read_csv('./data/new_post_SuicideWatch_240420.csv', sep=";")
]).reset_index()



app.layout = html.Div(
    [
        html.Div("This app is made to generate a wordcloud based on the words with the highest frequency in fives French newspapers",
                 style={'textAlign': 'center', 'fontSize': 20, 'fontWeight': 'bold'}),
        html.Div(dcc.Dropdown(subreddits,
                            multi=True,
                            placeholder="Please select relevant subreddits",
                            id="subreddit-dropdown",
                            value=list(subreddits),
                            style={'width': '700px', 'margin': 'auto'}
                            ),
                 style={'padding': '15px 0px'}),
        dmc.Text(id='time-text', weight=100, size=20, align="center", underline=True),
        dcc.Loading(
            id="loading-wordcloud",
            children=dcc.Graph(id="wordcloud"),
            type="circle",
            color="#ff4500"
        )

    ]
)

@app.callback(
    Output("wordcloud","figure"),
    Input("subreddit-dropdown","value")
)

def generate_wordcloud(sub_list):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    reddit_mask = np.array(Image.open('./masks/color_palette.png'))
    colors = ImageColorGenerator(reddit_mask)
    brain_mask = np.array(Image.open('./masks/brain.jpg'))
    data = filter_data(all_merged, sub_list)
    data.loc[:, 'texte'] = data['texte'].astype(str)
    text_string = ' '.join(data['texte'])
    wordcloud = WordCloud(background_color='white',mask=brain_mask,color_func=colors).generate(text_string)
    fig = go.Figure()
    fig.add_trace(go.Image(z=wordcloud.to_array()))
    fig.update_layout(
        autosize=False,
        width=1500,
        height=768,
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

        