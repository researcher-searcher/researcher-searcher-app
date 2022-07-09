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
from loguru import logger

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Br(),
                                html.Img(
                                    src=app.get_asset_url("overview-images.png"),
                                    style={"width": "100%"},
                                ),
                                dcc.Markdown(
                                    """
                    ### Search

                    ##### 5 methods:
                    
                    1. **Combine:** Combination of 2 and 3. Score for 3 is multiplied by 30 and added to score from 2. 
                    Aim of this method is to capture the benefits of both approaches, boost the results from full text, and allow 
                    for results only identified by vectors.

                    2. **Full text:** Query text is split into sentences. 
                    Each sentence is queried against each title/abstract sentences using the 
                    Elasticsearch full text [similarity score](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) 
                    (limit top 100).  Weighted average returned for 
                    each person using score and rank multiplied by a value representing the number of matching sentences.
                    
                    3. **Vector:** Query text is split into sentences. 
                    A vector\* representation of each sentence is created then 
                    compared to the vectors\* of all title/abstract sentences 
                    using cosine distance (limit top 100).  Weighted average 
                    returned for each person using distance and rank multiplied by a value representing the number of matching sentences.
                    
                    4. **Person:** Query text is treated as single document 
                    and a single vector\* is created. This is compared to each 
                    person vector\* (average of output sentences) using cosine 
                    distance and top 100 returned.
                    
                    5. **Output:** Query text is treated as single document and a 
                    single vector\* is created. This is compared to each output vector\* 
                    (average of output sentences) using cosine distance and top 100 
                    returned.

                    ### Person

                    For a given person, returns a summary of [Spacy noun chunks](https://spacy.io/usage/linguistic-features#noun-chunks) identified from 
                    all associated sorted by the [TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) score.

                    ### Collaboration

                    For a given person, returns the most similar people as defined by average sentence vectors\*. 
                    
                    ##### Three filter options:
                    
                    1. **Shared output:** Return only people with a shared output
                    
                    2. **No shared output:** Return only people with no shared output
                    
                    3. **All:** Return all people
                    
                    ***

                    \*All vectors were created using [Google Universal Sentence Encoder via Spacy](https://spacy.io/universe/project/spacy-universal-sentence-encoder)

                    """
                                ),
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)
