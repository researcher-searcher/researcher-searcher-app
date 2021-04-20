import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps.search import api_search
from functions import api_search, api_person, api_collab
from app import app
from apps import home, search, person, collaboration

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)
    if pathname == '/search':
        return search.layout
    elif pathname == '/person':
        return person.layout
    elif pathname == '/collaboration':
        return collaboration.layout
    else:
        return home.layout

# callback for search page
@app.callback(Output('search-table', 'data'),
              Input('search-submit-button-state', 'n_clicks'),
              State('search-input-1-state', 'value'),
              State('search-input-2-state', 'value'),
              )
def run_search(n_clicks, input1, input2):
    df = api_search(text=input1,method=input2)
    return df.to_dict('records')

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


if __name__ == '__main__':
    app.run_server(debug=True)
