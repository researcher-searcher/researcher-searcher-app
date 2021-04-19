import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps.search import api_search


from app import app
from apps import home, search

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
    #elif pathname == '/apps/app2':
    #    return app2.layout
    else:
        return home.layout

# callback for search page
@app.callback(Output('table', 'data'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'),
              )
def run_search(n_clicks, input1, input2):
    df = api_search(text=input1,method=input2)
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
