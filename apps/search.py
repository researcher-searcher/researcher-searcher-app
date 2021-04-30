import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_table
import itertools
import plotly.express as px
from dash.dependencies import Input, Output, State
from app import app, navbar, footer
from functions import api_search
from loguru import logger
from environs import Env

env = Env()
env.read_env()

# load extra layouts
cyto.load_extra_layouts()

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - UoB Data Science Network"

# API globals
#API_URL = "https://bdsn-api.mrcieu.ac.uk"
API_URL = env.str("API_URL")
logger.info(f'Using API: {API_URL}')
starter_query="logistic regression. genome wide association studies"
#starter_query="nematode. deep learning"
#starter_query="""
#Results from genome-wide association studies (GWAS) can be used to infer causal relationships between phenotypes, using a strategy known as 2-sample Mendelian randomization (2SMR) and bypassing the need for individual-level data. However, 2SMR methods are evolving rapidly and GWAS results are often insufficiently curated, undermining efficient implementation of the approach. We therefore developed MR-Base (http://www.mrbase.org): a platform that integrates a curated database of complete GWAS results (no restrictions according to statistical significance) with an application programming interface, web app and R packages that automate 2SMR. The software includes several sensitivity analyses for assessing the impact of horizontal pleiotropy and other violations of assumptions. The database currently comprises 11 billion single nucleotide polymorphism-trait associations from 1673 GWAS and is updated on a regular basis. Integrating data with software ensures more rigorous application of hypothesis-driven analyses and allows millions of potential causal relationships to be efficiently evaluated in phenome-wide association studies.
#"""
starter_method="combine"

# get some data to start with
df  = api_search(text=starter_query,method=starter_method).head(n=50)

def create_graph_data():
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
    return element_data

def create_xy():
    fig = px.scatter(
        df.head(n=50), x="WA", y="Top Score",hover_data=['Name'],size='Count',color='Org',symbol='Org',
        labels={
                "WA": "Weighted Average (WA)",
                },
        title="Top 50 people"
        )
    return fig

fig = create_xy()

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
                            {'label': 'Combine', 'value': 'combine'},
                            {'label': 'Full text search', 'value': 'full'},
                            {'label': 'Vector search', 'value': 'vec'},
                            {'label': 'Person search', 'value': 'person'},
                            {'label': 'Output search', 'value': 'output'}
                        ],
                        value='combine',
                        id='search-input-2-state'
                    ),
                ]),
                dbc.Col([
                    html.Br(),
                    html.Button(id='search-submit-button-state', n_clicks=0, children='Submit',style={"padding": "10px"}),
                    
                ])
            ]),
            # dbc.Row([
            #     dbc.Col([
            #         cyto.Cytoscape(
            #             id='rs-search',
            #             layout={
            #                 'name': 'cose',
            #                 'nodeRepulsion': 450000,
            #                 'gravitys' : 5    
            #                 },
            #             style={'width': '100%', 'height': '800px'},
            #             elements = element_data,
            #             stylesheet=[
            #                 # Group selectors
            #                 {
            #                     'selector': 'node',
            #                     'style': {
            #                         'content': 'data(label)',
            #                         'text-halign':'center',
            #                         'text-valign':'center',
            #                         'width':'label',
            #                         'height':'label',
            #                         'shape':'circle',
            #                         "text-wrap": "wrap",
            #                         "text-max-width": 80
            #                     }
            #                 },

            #                 # Class selectors
            #                 {
            #                     'selector': '.name',
            #                     'style': {
            #                         'background-color': '#D4E4F7',
            #                     }
            #                 },
            #                 {
            #                     'selector': '.output',
            #                     'style': {
            #                         'background-color': '#FDA15A',
            #                     }
            #                 },
            #                 {
            #                     'selector': '.org',
            #                     'style': {
            #                         'background-color': '#E1EF83',
            #                     }
            #                 },
            #                 {
            #                     'selector': '.query_sentences',
            #                     'style': {
            #                         'background-color': '#FF9EB5',
            #                     }
            #                 },
            #             ]
            #         ),
            #     ]),
            # ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='search-fig',
                        figure=fig,
                        responsive=True,
                        style={'height': '60vh'}
                    ),
                    dcc.Slider(
                        id='search-slider',
                        min=10,
                        max=100,
                        step=10,
                        value=50,
                        marks={ 0: '0', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50', 60: '60', 70: '70', 80: '80', 90: '90', 100: '100'},
                    ),
                    html.Div(id='search-slider-div')
                ])
            ]),
            dbc.Row([
                dbc.Col([    
                    html.Br(),
                    dash_table.DataTable(
                        id='search-table',
                        columns=[
                            {"name": i, "id": i} for i in df.columns
                        ],
                        #tooltip_data= [{c:{'type': 'text', 'value': f'{r},{c}'} for c in df.columns} for r in df[df.columns].values],
                        #tooltip_data= [   {
                        #    column: {'value': str(value), 'type': 'markdown'}
                        #        for column, value in row.items()
                        #    } for row in df.to_dict('records')
                        #],
                        #tooltip_delay=0,
                        #tooltip_duration=None,
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0
                        },
                        style_cell_conditional=[
                            {'if': 
                                {'column_id': 'Title'},
                                'width': '80%'
                            },
                            {'if':
                                {'column_id': 'Name'},
                                'width': '25%'
                            }
                        ],
                        data=df.to_dict('records'),
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current= 0,
                        page_size= 10,
                        export_format="csv",
                        filter_action='native',
                    ) 
                ])
            ]),
        ]),
        footer
    ])
