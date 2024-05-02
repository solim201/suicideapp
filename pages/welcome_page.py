import dash
import dash_mantine_components as dmc
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import pandas as pd
import os

dash.register_page(
    __name__,
    path='/welcome_page',
    order=0,
    title='Mental Health - Welcome page',
    description="""
    """,
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
all_merged = pd.read_csv('./data/all_sub_suicide.csv',sep=";")

subreddits = all_merged["forum"].unique()
options = [{'label': 'All Thread Together', 'value': 'all_thread_together'}]
options.extend({'label': subreddit, 'value': subreddit} for subreddit in subreddits)
sub_desc = {
    "mentalhealth": "A subreddit dedicated to discussing various aspects of mental health, including coping mechanisms, support, and personal experiences related to mental well-being.",
    "depression_help": f"This subreddit is focused on providing support, advices, and resources for individuals dealing with depression. Members share their experiences and offer assistance to those in need of help.",
    "SuicideBereavement": "A community for individuals who have lost loved ones to suicide. Members offer support, share coping strategies, and provide a space for processing grief and healing after experiencing such a loss.",
    "SuicideWatch": "A subreddit dedicated to providing support and intervention for individuals who are struggling with suicidal thoughts or feelings. Members offer empathy, encouragement, and resources to help those in crisis find hope and support.",
    "all_thread_together" : " "
            }

k_user_number = {
                'mentalhealth':457,
                'depression_help':95,
                'SuicideBereavement':37,
                'SuicideWatch':474,
                'all_thread_together': 1063
                }

def filter_data(all_merged,sub_list) :
    filtered_df = all_merged[all_merged['forum'] == sub_list]
    return filtered_df

def count_rows(df) :
    number_of_post = df.shape[0]
    return number_of_post

def count_comments(df) :
    number_of_comments = df['nb_commentaires'].sum()
    return number_of_comments

dash.register_page(
    __name__,
    path='/',
    order=0,
    title='Mental Health - Welcome page',
    description="""
    """,
)

title_style = {"textAlign" : "center"}
semititle_style = {"textAlign" : "center"}
layout = html.Div([
    dmc.Grid(
            dmc.Col(
                dmc.Title('Welcome to our Reddit Insights Explorer !')
                ,style=title_style)
            ),
    dmc.Grid(
        dmc.Col([
                dmc.Text("Our goal is to explore reddit's depths to identify subreddits linked to suicidals tendencies",size="xl"),
                dmc.Text("In this purpose we analyse differents post and their comments within differents subreddits",size="xl")
                ],style=semititle_style)
    ),
    dmc.Grid(
        dmc.Col([
            dmc.Text("You can click down bellow to select the subreddits you want to explore :",style = semititle_style),
            dcc.Dropdown(options=options,
                         multi=False, #True  #If need to be multiple
                         placeholder = "Please select relevants subreddits",
                         id ="subreddit-dropdown",
                         style={'width': '600px','margin-left': 'auto', 'margin-right': 'auto'}
                         ),
        ])
    ,style={"padding":"40px 0px 0px 0px"}),
    dmc.Grid(
            dmc.Col(
                html.Div(dmc.Text(id="description",ta="center"),style={'border': "2px solid #FCA57A"})
                ,span=6)
        ,align="center",justify='center'),
    dmc.Grid(
        [
            dmc.Col(
                dbc.Card([
                    dbc.CardHeader(dmc.Text("Number of subscribers:")),
                    dbc.CardBody(dmc.Text("0",id="box1",weight=900,ta="center",size="xl")),
                    ]),span=3
                ),
            dmc.Col(dbc.Card([
                    dbc.CardHeader(dmc.Text("Number of posts found:")),
                    dbc.CardBody(dmc.Text("0",id="box2",weight=900,ta="center",size="xl")),
                        ]),span=3),
            dmc.Col(dbc.Card([
                    dbc.CardHeader(dmc.Text("Number of comments:")),
                    dbc.CardBody(dmc.Text("0",id="box3",weight=900,ta="center",size="xl"))
                        ]),span=3)

        ],align="center",justify='center',gutter='50',style={"padding":"30px 60px 30px"}
    ),
    html.Div(dmc.Center(dmc.Image(src='assets/logo.png', height="60px", width="60px")))
],style={'padding':'30px 0px 60px 0px'},className='animate__animated animate__fadeIn animate__slow')


@callback(
    Output("box1","children"),
    Output("box2","children"),
    Output("box3","children"),
    Output("description","children"),
    Input("subreddit-dropdown","value")
)

def update_box(selection) :
    if selection is None:
        raise PreventUpdate
    elif selection == 'all_thread_together':
        total_users = k_user_number[selection]
        nb_posts = count_rows(all_merged)
        nb_comments = count_comments(all_merged)
        description = sub_desc[selection]
        return str(total_users)+" K",nb_posts,nb_comments,description
    else :
        filtered_data = filter_data(all_merged,selection)
        total_users = k_user_number[selection]
        """for forum in selection:
            total_users += k_user_number.get(forum, 0)""" #If need to be multiple
        nb_posts = count_rows(filtered_data)
        nb_comments = count_comments(filtered_data)
        description = sub_desc[selection]
        return str(total_users)+" K",nb_posts,nb_comments,description