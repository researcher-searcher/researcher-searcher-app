import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from app import app, navbar, footer
from functions import api_person

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

# API globals
starter_query="https://research-information.bris.ac.uk/en/persons/jean-golding"

# get some data to start with
df  = api_person(text=starter_query)

layout = html.Div([
        navbar,
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5('Query:'),
                    dbc.Input(
                        id='person-input-1-state', 
                        type='text',
                        value=starter_query)
                ],width=6),
                dbc.Col([
                    html.Br(),
                    html.Button(id='person-submit-button-state', n_clicks=0, children='Submit',style={"padding": "10px"}),
                ]),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dcc.Loading(
                        id="person-loading-1",
                        type="default",
                        children=html.Div(id="person-loading-output-1")
                    ),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dash_table.DataTable(
                        id='person-table',
                        columns=[
                            {"name": i, "id": i} for i in df.columns
                        ],
                        data=df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        export_format="csv"
                    ),
                ])
            ])
        ]),
        footer
    ])
