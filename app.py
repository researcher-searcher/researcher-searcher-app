import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import requests

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

API_URL = "https://bdsn-api.mrcieu.ac.uk"

def search(text:str,method:str):
    endpoint = "/search/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": method
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    df['org'] = df['org'].str[:1]
    return df[['person_name','count','org','wa']]

starter_query="graph database"
starter_method="full"
df  = search(text=starter_query,method=starter_method)

def layout_function():
    return html.Div([
        dbc.Container([
            dbc.Row([
                html.H1('Researcher Searcher - UoB Data Science Network'),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Label('Query:'),
                    dbc.Textarea(
                        id='input-1-state', 
                        value=starter_query,
                        style={'width': '100%', 'height': 100}
                    )
                ]),
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Label('Method:'),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Full text search', 'value': 'full'},
                            {'label': 'Vector search', 'value': 'vec'},
                            {'label': 'Person search', 'value': 'person'},
                            {'label': 'Output search', 'value': 'output'}
                        ],
                        value='full',
                        id='input-2-state'
                    ),
                ]),
                dbc.Col([
                    html.Br(),
                    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dash_table.DataTable(
                        id='table',
                        columns=[
                            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
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

app.layout = layout_function

@app.callback(Output('table', 'data'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'),
              )
def run_search(n_clicks, input1, input2):
    df = search(text=input1,method=input2)
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)