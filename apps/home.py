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
from functions import api_vector
from sklearn.manifold import TSNE

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

#PEOPLE_VECTORS = 'data/people_vectors.pkl.gz'
PEOPLE_PAIRS = 'data/people_vector_pairs.pkl.gz'
TSNE_DF = 'data/tsne.csv.gz'

df = pd.read_csv(TSNE_DF)
df.drop_duplicates(inplace=True)
org_counts = df['org-name'].value_counts()

# filter df to top X for plot
df['org_count']= df['org-name'].map(org_counts)
df['org-name'] = df['org-name']+' '+df['org_count'].astype(str)

logger.info(f'\n{org_counts}')
logger.info(f'\n{df}')

vec_data = api_vector(text='data science')
logger.info(vec_data)

tSNE=TSNE(n_components=2)


def run_tsne():
    pp_df=pd.read_pickle(PEOPLE_PAIRS)
    logger.info(pp_df.shape)

    summary_df = pd.read_csv(TSNE_DF)
    pp_df = pp_df[(pp_df['email1'].isin(summary_df['email'])) & (pp_df['email2'].isin(summary_df['email']))]
    logger.info(pp_df.shape)

    #logger.info(df.head())
    pp_df_pivot = pp_df.pivot(index='email1', columns='email2', values='score')
    logger.info(pp_df_pivot.shape)
    pp_df_pivot = pp_df_pivot.fillna(1)
    tSNE_result=tSNE.fit_transform(pp_df_pivot)
    x=tSNE_result[:,0]
    y=tSNE_result[:,1]
    summary_df['x']=x
    summary_df['y']=y
    logger.info(summary_df.shape)

run_tsne()

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