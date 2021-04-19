import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
        #print(search.app.layout())
        return search.app.layout()
    #elif pathname == '/apps/app2':
    #    return app2.layout
    else:
        return home.app.layout
        

if __name__ == '__main__':
    app.run_server(debug=True)
