import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
from functions import api_collab
from environs import Env

env = Env()
env.read_env()

dash.register_page(__name__)

example_person = env.str("EXAMPLE_PERSON")
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# get some data to start with
df = api_collab(text=example_person)

layout = html.Div(
    [
        dbc.Container(
            [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Query:"),
                                dbc.Input(
                                    id="collab-input-1-state",
                                    type="text",
                                    value=example_person,
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.H5("Method:"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Shared output", "value": "yes"},
                                        {"label": "No shared output", "value": "no"},
                                        {"label": "All", "value": "all"},
                                    ],
                                    value="no",
                                    id="collab-input-2-state",
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Br(),
                                html.Button(
                                    id="collab-submit-button-state",
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
                                    id="collab-loading-1",
                                    type="default",
                                    children=html.Div(id="collab-loading-output-1"),
                                ),
                            ]
                        ),
                    ]
                ),
                # dbc.Row([
                #    dbc.Col([
                #        dcc.Graph(
                #            id='collab-plot',
                #            figure=fig,
                #            responsive=True,
                #            style={'height': '80vh'}
                #        )
                #    ])
                # ]),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Br(),
                                dash_table.DataTable(
                                    id="collab-table",
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
    ]
)
