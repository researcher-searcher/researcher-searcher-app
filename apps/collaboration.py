import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from app import app, navbar
from functions import api_collab

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

# API globals
starter_query="jean.golding@bristol.ac.uk"

# get some data to start with
df  = api_collab(text=starter_query)

layout = html.Div([
        navbar,
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Query:'),
                    dbc.Input(
                        id='collab-input-1-state', 
                        type='text',
                        value=starter_query                    )
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5 ('Method:'),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Shared output', 'value': 'yes'},
                            {'label': 'No shared output', 'value': 'no'},
                            {'label': 'All', 'value': 'all'}                        ],
                        value='yes',
                        id='collab-input-2-state'
                    ),
                ]),
                dbc.Col([
                    html.Br(),
                    html.Button(id='collab-submit-button-state', n_clicks=0, children='Submit'),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dash_table.DataTable(
                        id='collab-table',
                        columns=[
                            {"name": i, "id": i} for i in df.columns
                        ],
                        data=df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                    ),
                    html.Div(id='datatable-interactivity-container')
                ])
            ])
        ])
    ])