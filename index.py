import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps.search import api_search
from functions import api_search, api_search_person, api_search_output, api_person, api_collab, run_tsne
from app import app, server
from apps import home, search, person, collaboration, about
from loguru import logger

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    logger.info(pathname)
    if pathname == '/search':
        return search.layout
    elif pathname == '/person':
        return person.layout
    elif pathname == '/collaboration':
        return collaboration.layout
    elif pathname == '/about':
        return about.layout
    else:
        return home.layout

# callback for search page
@app.callback(Output('search-table', 'data'),
              Output('search-table', 'columns'),
              Input('search-submit-button-state', 'n_clicks'),
              State('search-input-1-state', 'value'),
              State('search-input-2-state', 'value'),
              )
def run_search(n_clicks, input1, input2):
    logger.info(f'{input1} {input2}') 
    if input2 in ['full','vec']:
        df = api_search(text=input1,method=input2)
    elif input2 == 'person':
        df = api_search_person(text=input1)
    elif input2 == 'output':
        df = api_search_output(text=input1)
    columns=[
            {"name": i, "id": i} for i in df.columns
        ]
    logger.debug(columns)
    return df.to_dict('records'), columns
    

# callback for person page
@app.callback(Output('person-table', 'data'),
              Input('person-submit-button-state', 'n_clicks'),
              State('person-input-1-state', 'value'),
              )
def run_person(n_clicks, input1):
    df = api_person(text=input1)
    return df.to_dict('records')

# callback for collab page
@app.callback(Output('collab-table', 'data'),
              Input('collab-submit-button-state', 'n_clicks'),
              State('collab-input-1-state', 'value'),
              State('collab-input-2-state', 'value'),
              )
def run_collab(n_clicks, input1, input2):
    df = api_collab(text=input1,method=input2)
    return df.to_dict('records')

# callback for home page
#@app.callback(Output('home-fig', 'figure'),
#              Input('home-submit-button-state', 'n_clicks'),
#              State('home-input-1-state', 'value'),
#              )
#def update_plot(n_clicks, input1):
#    fig = run_tsne(query=input1)
#    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)
