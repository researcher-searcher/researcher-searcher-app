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

# load extra layouts
cyto.load_extra_layouts()

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

# API globals
API_URL = "https://bdsn-api.mrcieu.ac.uk"
starter_query="logistic regression. genome wide association studies"
#starter_query="nematode. deep learning"
#starter_query="""
#Results from genome-wide association studies (GWAS) can be used to infer causal relationships between phenotypes, using a strategy known as 2-sample Mendelian randomization (2SMR) and bypassing the need for individual-level data. However, 2SMR methods are evolving rapidly and GWAS results are often insufficiently curated, undermining efficient implementation of the approach. We therefore developed MR-Base (http://www.mrbase.org): a platform that integrates a curated database of complete GWAS results (no restrictions according to statistical significance) with an application programming interface, web app and R packages that automate 2SMR. The software includes several sensitivity analyses for assessing the impact of horizontal pleiotropy and other violations of assumptions. The database currently comprises 11 billion single nucleotide polymorphism-trait associations from 1673 GWAS and is updated on a regular basis. Integrating data with software ensures more rigorous application of hypothesis-driven analyses and allows millions of potential causal relationships to be efficiently evaluated in phenome-wide association studies.
#"""
starter_method="full"

# get some data to start with
df  = api_search(text=starter_query,method=starter_method)

# get unique elements for nodes
top=50
node_data = {
    'name':list(df['Name'].head(n=top).unique()),
    'query_sentences':list(set(itertools.chain.from_iterable(df.head(n=top)['q_sent_text']))),
    #'match_sentences':list(set(itertools.chain.from_iterable(df.head(n=top)['m_sent_text']))),
    'org':list(set(itertools.chain.from_iterable(df.head(n=top)['Org']))),
    #'output':list(set(itertools.chain.from_iterable(df.head(n=top)['output'])))
}

element_data=[]
for k in node_data:
    #logger.debug(k)
    for v in node_data[k]:
        #logger.debug(f'{k} {v}')
        element_data.append(
            {'data': {'id': v, 'label': v[:30]}, 'classes':k},
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
            #{'data': {'source': row['output'][j], 'target':row['Name']}},
        ])


#logger.debug(element_data)
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
                        id='rs-search',
                        layout={
                            'name': 'cose',
                            'nodeRepulsion': 450000,
                            'gravitys' : 5    
                            },
                        style={'width': '100%', 'height': '800px'},
                        elements = element_data,
                        stylesheet=[
                            # Group selectors
                            {
                                'selector': 'node',
                                'style': {
                                    'content': 'data(label)',
                                    'text-halign':'center',
                                    'text-valign':'center',
                                    'width':'label',
                                    'height':'label',
                                    'shape':'circle',
                                    "text-wrap": "wrap",
                                    "text-max-width": 80
                                }
                            },

                            # Class selectors
                            {
                                'selector': '.name',
                                'style': {
                                    'background-color': '#D4E4F7',
                                }
                            },
                            {
                                'selector': '.output',
                                'style': {
                                    'background-color': '#FDA15A',
                                }
                            },
                            {
                                'selector': '.org',
                                'style': {
                                    'background-color': '#E1EF83',
                                }
                            },
                            {
                                'selector': '.query_sentences',
                                'style': {
                                    'background-color': '#FF9EB5',
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
