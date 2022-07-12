import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app, navbar, footer
from functions import api_person
from environs import Env

env = Env()
env.read_env()

example_person = env.str("EXAMPLE_PERSON")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# get some data to start with
df = api_person(text=example_person)
#df = pd.DataFrame() 

options=[html.Option(value=x) for x in ["Chocolate", "Coconut", "Mint", "Strawberry"]]

layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Query:"),
                                    dbc.Input(
                                        id=dict(type='searchData', id='dest-loc'),
                                        list='list-suggested-inputs',
                                        placeholder="Enter Name...",
                                        persistence=False,
                                        autocomplete="off",
                                    ),
                                    html.Datalist(id='list-suggested-inputs', children=[html.Option(value='')]),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.Br(),
                                html.Button(
                                    id="person-submit-button-state",
                                    n_clicks=0,
                                    children="Submit",
                                    style={"padding": "10px"},
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Br(),
                                html.Br(),
                                dcc.Loading(
                                    id="person-loading-1",
                                    type="default",
                                    children=html.Div(id="person-loading-output-1"),
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Br(),
                                dash_table.DataTable(
                                    id="person-table",
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    data=df.to_dict("records"),
                                    sort_action="native",
                                    sort_mode="multi",
                                    page_action="native",
                                    page_current=0,
                                    page_size=10,
                                    export_format="csv",
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        footer,
    ]
)
