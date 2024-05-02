import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go
import os
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
from PIL import Image

# Préenregistrement de l'emplacement
os.chdir(os.path.dirname(os.path.abspath(__file__)))


dash.register_page(
    __name__,
    path='/page2',
    order=2,
    title='Mental Health - In depths analysis',
    description="""
    """,
)

all_merged = pd.read_csv('./data/all_sub_suicide.csv',sep=";")

def filter_data(all_merged,sub_list) :
    filtered_df = all_merged[all_merged['forum'].isin(sub_list)]
    return filtered_df

subreddits = all_merged["forum"].unique()#['all_together','depression_help','mentalhealth','SuicideBereavement','SuicideWatch']
all_merged = pd.read_csv('./data/all_sub_suicide.csv',sep=";")

def filter_data(all_merged,sub_list) :
    filtered_df = all_merged[all_merged['forum'].isin(sub_list)]
    return filtered_df

subreddits = all_merged["forum"].unique()#['all_together','depression_help','mentalhealth','SuicideBereavement','SuicideWatch']

title_style = {"textAlign" : "center"}
semititle_style = {"textAlign" : "center"}

layout = html.Div([
            dmc.Title('Detection of suicidal comments by AI',style= title_style),
            dmc.Text('Here we are trying an experimental approch of moderation, by using AI to classify comments as "suicidal" or "not suicidal"',style=title_style),
            dmc.Text('We used Mistral 7B, the most powerful open-source model for its size (7 billion parameters). We sent it nearly 11,000 comments, which it processed in a little less than 8 hours and 30 minutes, with an average response time of 2.73 seconds per message.',style=title_style),
            dmc.Text('We are aware that this is not its primary use and that therefore errors will be present, but we found it interesting to use a tool made available to everyone for automatic text classification.',style= title_style),
            html.Div(dcc.Dropdown(subreddits,
                            multi=True,
                            placeholder = "Please select relevants subreddits",
                            id ="subreddit-dropdown_bis",
                            value=list(subreddits),
                            style={'width': '700px','margin-left': 'auto', 'margin-right': 'auto'}

                            ),
                            style={'padding':'15px 0px 0px 0px'}
                        ),

            dmc.Grid([
                dmc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            dmc.Text("Number of posts within the subs :",weight=900,size="xl")
                            ),
                        dbc.CardBody(
                            dcc.Loading(
                                    id="loading-posts_curve",
                                    children=dcc.Graph(id="posts-curve_bis"),
                                    type="circle",
                                    color="#ff4500")
                            ),
                        ],className='rounded'
                    )
                    ,span=11,style={'padding':'20px 0px'})
                ],
                align="center",justify='center'
            ),
            dmc.Grid([
                dmc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            dmc.Text("Number of posts by day of the week :",weight=900,size="xl")
                            ),
                        dbc.CardBody(
                            dcc.Loading(
                                    id="loading-posts_by_day",
                                    children=dcc.Graph(id="posts_by_day_bis"),
                                    type="circle",
                                    color="#ff4500")
                            ),
                        ],
                        className='rounded'
                    )
                    ,span=5,style={'padding':'20px 20px 0px 0px'}
                ),
                dmc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            dmc.Text("Number of posts by time of day:",weight=900,size="xl")
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-posts_by_time",
                                    children=dcc.Graph(id="posts_by_time_bis"),
                                    type="circle",
                                    color="#ff4500")
                            ),
                        ],
                        className='rounded'
                    )
                ,span=5,style={'padding':'20px 0px 0px 20px'}
                )
            ],align="center",justify='center'),
            dmc.Grid([
                dmc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            dmc.Text("Most frequents words for comments classified as suicidal:",weight=900,size="xl")
                            ),
                        dbc.CardBody(
                            dmc.Center(
                                dcc.Loading(
                                    id="loading-wordcloud",
                                    children=dcc.Graph(id="wordcloud_bis",config={'scrollZoom' : True,'autosizable' : True},style={"width": "100%", "height": "600px"}),
                                    type="circle",
                                    color="#ff4500"
                                    )
                                )
                            ),
                        ],className='rounded'
                    )
                    ,span=8,style={'padding':'40px 0px'})
                ],
                align="center",justify='center'
            )
        ],style={'padding':'20px  0px'}
    )

@callback(
    Output('posts-curve_bis','figure',),
    Output('posts_by_day_bis','figure'),
    Output('posts_by_time_bis','figure'),
    Output("wordcloud_bis","figure"),
    Input('subreddit-dropdown_bis','value')
            )

def update_graphs(valeur):
    data = filter_data(all_merged, valeur)

    #global df building
    data = filter_data(all_merged, valeur)
    df_global = data.groupby('date_post').size().reset_index(name='nb_posts')
    df_global_suicide = data[data['suicidal_thought_binary']=="yes"].groupby('date_post').size().reset_index(name='nb_posts')

    #days df building
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data['jour_post'] = pd.Categorical(data['jour_post'], categories=days_order, ordered=True)
    df_days = data.groupby('jour_post',observed=False).size().reset_index(name='nb_posts')
    df_days_suicide = data[data['suicidal_thought_binary']=="yes"].groupby('jour_post',observed=False).size().reset_index(name='nb_posts')

    #hours df building
    data['heure_post'] = pd.to_datetime(data['heure_post'],format='%H:%M:%S').dt.hour
    df_hours = data.groupby('heure_post',observed=False).size().reset_index(name='nb_posts')
    df_hours_suicide = data[data['suicidal_thought_binary']=="yes"].groupby('heure_post',observed=False).size().reset_index(name='nb_posts')
    #ploting
    fig_global = go.Figure([go.Scatter(x=df_global['date_post'], y=df_global['nb_posts'],line=dict(color='#0008ff'),name="all comments",fill='tozeroy'),go.Scatter(x=df_global['date_post'], y=df_global_suicide['nb_posts'],line=dict(color='#ff4500'),name="Suicidal comments",fill='tozeroy' )])
    fig_global.update_layout(title='',
                    xaxis_title='Date',
                    yaxis_title='Number of posts',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False),
                    plot_bgcolor='rgba(0,0,0,0)')


    fig_days = go.Figure([go.Scatter(x=df_days['jour_post'], y=df_days['nb_posts'],line=dict(color='#0008ff'),name="all comments",fill='tozeroy'),go.Scatter(x=df_days['jour_post'], y=df_days_suicide['nb_posts'],line=dict(color='#ff4500'),name="Suicidal comments",fill='tozeroy')])
    fig_days.update_layout(title='',
                    xaxis_title='Day of the week',
                    yaxis_title='Number of posts',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False),
                    plot_bgcolor='rgba(0,0,0,0)')

    fig_hours = go.Figure([go.Scatter(x=df_hours['heure_post'],y=df_hours['nb_posts'],line=dict(color='#0008ff'),name="all comments",fill='tozeroy'),go.Scatter(x=df_hours['heure_post'],y=df_hours_suicide['nb_posts'],line=dict(color='#ff4500'),name="Suicidal comments",fill='tozeroy')])
    fig_hours.update_layout(title='',
                xaxis_title='Hour of the day',
                yaxis_title='Number of posts',
                xaxis=dict(
                      tickmode='linear',
                      tick0=0,
                      dtick=1,
                      showgrid=False),
                yaxis=dict(showgrid=False),
                plot_bgcolor='rgba(0,0,0,0)'
            )
    #wordcloud data management + generation
    data_suicide = data[data['suicidal_thought_binary']=="yes"]
    data_suicide.loc[:, 'texte'] = data_suicide['texte'].astype(str)
    text_string = ' '.join(data_suicide['texte'])
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
    human_mask = np.array(Image.open('./masks/color_palette.png'))
    reddit_mask =  np.array(Image.open('./masks/hm.jpg'))
    colors = ImageColorGenerator(human_mask)
    wordcloud = WordCloud(background_color='white',mask=reddit_mask,contour_width=0,color_func=colors).generate(text_string)
    fig_wordcloud = go.Figure()
    fig_wordcloud.add_trace(go.Image(z=wordcloud.to_array()))
    fig_wordcloud.update_layout(showlegend=False)
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_global,fig_days,fig_hours,fig_wordcloud

