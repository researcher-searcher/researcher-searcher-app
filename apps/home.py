import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import requests
import numpy as np
import pandas as pd
from app import app, navbar
from loguru import logger

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

df = pd.read_csv('data/tsne.csv.gz')
df.drop_duplicates(inplace=True)
org_counts = df['org-name'].value_counts()

# filter df to top X for plot
df['org_count']= df['org-name'].map(org_counts)
df['org-name'] = df['org-name']+' '+df['org_count'].astype(str)

logger.info(f'\n{org_counts}')
logger.info(f'\n{df}')

def plotly_scatter_plot(df,top=12):
    df = df[df['org_count']>top]
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        color="org-name",
        symbol="org-name",
        hover_data=['email']
        )
    fig.update_layout(legend_title_text=f'Organisation (>{top} people)')
    return fig

fig = plotly_scatter_plot(df)

layout = html.Div([
        navbar,
        dbc.Container([
            dcc.Graph(
                figure=fig,
                responsive=True,
                style={'height': '80vh'}
            )
        ])
    ])