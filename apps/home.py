import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import requests
import numpy as np
import pandas as pd
from app import app, navbar, footer
from loguru import logger
from functions import api_vector, plotly_scatter_plot, run_tsne

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])


def read_tsne():
    TSNE_DF = 'data/tsne.csv.gz'

    df = pd.read_csv(TSNE_DF)
    df['origin']='tsne'
    df.drop_duplicates(inplace=True)
    org_counts = df['org-name'].value_counts()

    # filter df to top X for plot
    df['org_count']= df['org-name'].map(org_counts)
    df['org-name'] = df['org-name']+' '+df['org_count'].astype(str)

    #logger.info(f'\n{org_counts}')
    #logger.info(f'\n{df}')
    return df

starter_query = 'data science. genome wide association studies'
#fig = run_tsne(starter_query)
df = read_tsne()
fig = plotly_scatter_plot(df)


layout = html.Div([
        navbar,
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='home-fig',
                        figure=fig,
                        responsive=True,
                        style={'height': '80vh'}
                    ),
                ])
            ]),
            # dbc.Row([
            #     dbc.Col([
            #         html.H5('Query:'),
            #         dbc.Input(
            #             id='home-input-1-state', 
            #             type='text',
            #             value=starter_query                    )
            #     ]),
            #     dbc.Col([
            #         html.Br(),
            #         html.Button(id='home-submit-button-state', n_clicks=0, children='Submit',style={"padding": "10px"}),
            #     ])
            # ]),
        ]),
        footer
    ])