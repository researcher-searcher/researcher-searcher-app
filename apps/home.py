import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import requests
import pandas as pd
from app import app, navbar
from loguru import logger

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

df = pd.read_csv('data/tsne.csv.gz')

def plotly_scatter_plot(df):
    fig = px.scatter(
        df, 
        x="x", 
        y="y", 
        color="org-name",
        hover_data=['email']
        )
    return fig

fig = plotly_scatter_plot(df)

layout = html.Div([
        navbar,
        dbc.Container([
            dcc.Graph(
                figure=fig,
                responsive=True
            )
        ])
    ])