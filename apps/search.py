import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_table
import itertools
from dash.dependencies import Input, Output, State
from app import app, navbar
from functions import api_search
from loguru import logger

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

# API globals
API_URL = "https://bdsn-api.mrcieu.ac.uk"
starter_query="logistic regression. genome wide association studies"
starter_method="full"

# get some data to start with
df  = api_search(text=starter_query,method=starter_method)

# get unique elements for nodes
top=5
node_data = {
    'name':list(df['Name'].head(n=top).unique()),
    'query_sentences':list(set(itertools.chain.from_iterable(df.head(n=top)['q_sent_text']))),
    #'match_sentences':list(set(itertools.chain.from_iterable(df.head(n=top)['m_sent_text']))),
    'org':list(set(itertools.chain.from_iterable(df.head(n=top)['Org']))),
    'output':list(set(itertools.chain.from_iterable(df.head(n=top)['output'])))
}

element_data=[]
for k in node_data:
    logger.debug(k)
    for v in node_data[k]:
        logger.debug(f'{k} {v}')
        element_data.append(
            {'data': {'id': v, 'label': v[:20]}, 'classes':k},
        )

# create links
for i,row in df.head(n=top).iterrows():
    element_data.append(
        {'data': {'source': row['Name'], 'target':row['Org'][0]}},
    )
    for j in range(len(row['scores'])):
        element_data.extend([
            {'data': {'source': row['Name'], 'target':row['q_sent_text'][j], "weight":row['scores'][j]}, "classes":"name-qsent"},
            #{'data': {'source': row['output'][j], 'target':row['m_sent_text'][j]}},
            {'data': {'source': row['output'][j], 'target':row['Name']}},
        ])
# make rels unique


logger.debug(element_data)
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
                    html.Button(id='search-submit-button-state', n_clicks=0, children='Submit',style={"padding": "10px"}),
                    
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    cyto.Cytoscape(
                        id='cytoscape-two-nodes',
                        layout={'name': 'cose'},
                        style={'width': '100%', 'height': '800px'},
                        #elements=[
                        #    {'data': {'id': 'one', 'label': 'Node 1'}},
                        #    {'data': {'id': 'two', 'label': 'Node 2'}},
                        #    {'data': {'source': 'one', 'target': 'two'}}
                        #]
                        elements = element_data,
                        stylesheet=[
                            # Group selectors
                            {
                                'selector': 'node',
                                'style': {
                                    'content': 'data(label)'
                                }
                            },

                            # Class selectors
                            {
                                'selector': '.name',
                                'style': {
                                    'background-color': 'red',
                                }
                            },
                            {
                                'selector': '.output',
                                'style': {
                                    'background-color': 'green',
                                }
                            },
                            {
                                'selector': '.org',
                                'style': {
                                    'background-color': 'blue',
                                }
                            },
                            {
                                'selector': '.query_sentences',
                                'style': {
                                    'background-color': 'orange',
                                }
                            },
                            
                            # {
                            #    'selector': '[weight > 3]',
                            #    'style': {
                            #        'line-color': 'blue'
                            #    }
                            #}
                        ]
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([    
                    html.Br(),
                    dash_table.DataTable(
                        id='search-table',
                        columns=[
                            {"name": i, "id": i} for i in df.columns
                        ],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0
                        },
                        style_cell_conditional=[
                            {'if': {'column_id': 'Title'},
                            'width': '80%'}
                        ],
                        data=df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        export_format="csv"
                    ) 
                ])
            ])
        ])
    ])
