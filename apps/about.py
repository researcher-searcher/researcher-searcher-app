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

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

layout = html.Div([
        navbar,
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    dcc.Markdown('''
                    ### Search

                    ##### 4 methods:
                    
                    1. **Full text:** Query test is split into sentences. 
                    Each sentence is queried against each title/abstract sentences using the 
                    Elasticsearch full text method (limit top 100).  Weighted average returned for 
                    each person using score and rank
                    
                    2. **Vector:** Query test is split into sentences. 
                    A vector representation of each sentence is created then 
                    compared to the vectors of all title/abstract sentences 
                    using cosine distance (limit top 100).  Weighted average 
                    returned for each person using distance and rank
                    
                    3. **Person:** Query text is treated as single document 
                    and a single vector is created. This is compared to each 
                    person vector (average of output sentences) using cosine 
                    distance and top 100 returned.
                    
                    4. **Output:** Query text is treated as single document and a 
                    single vector is created. This is compared to each output vector 
                    (average of output sentences) using cosine distance and top 100 
                    returned.

                    ### Person

                    For a given person, returns a summary of noun chunks identified from 
                    all associated output using the [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) score.

                    ### Collaboration

                    For a given person, returns the most similar people as defined by average sentence vectors. 
                    
                    ##### Three filter options:
                    
                    1. **Shared output:** Return only people with a shared output
                    
                    2. **No shared output:** Return only people with no shared output
                    
                    3. **All:** Return all people
                    
                    ***

                    For more information on the construction of this data set, see 
                    this GitHub repository - https://github.com/elswob/researcher-searcher-jgi

                    ''')
                ])
            ])
        ])
    ])