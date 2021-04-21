import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from app import app, navbar
from functions import api_search

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

# API globals
API_URL = "https://bdsn-api.mrcieu.ac.uk"
starter_query="logistic regression"
starter_method="full"

# get some data to start with
df  = api_search(text=starter_query,method=starter_method)

layout = html.Div([
        navbar,
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Query:'),
                    #html.P('Examples: '),
                    #html.Span(id='eg1',children='machine learning'),
                    dbc.Textarea(
                        id='search-input-1-state', 
                        value=starter_query,
                        style={'width': '100%', 'height': 100}
                    )
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5 ('Method:'),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Full text search', 'value': 'full'},
                            {'label': 'Vector search', 'value': 'vec'},
                            {'label': 'Person search', 'value': 'person'},
                            {'label': 'Output search', 'value': 'output'}
                        ],
                        value='full',
                        id='search-input-2-state'
                    ),
                ]),
                dbc.Col([
                    html.Br(),
                    html.Button(id='search-submit-button-state', n_clicks=0, children='Submit'),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dash_table.DataTable(
                        id='search-table',
                        columns=[
                            {"name": i, "id": i} for i in df.columns
                        ],
                        data=df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        export_format="csv",
                    ) 
                ])
            ])
        ])
    ])
