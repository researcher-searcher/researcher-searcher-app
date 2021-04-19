import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import requests

import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

API_URL = "https://bdsn-api.mrcieu.ac.uk"

def search(text:str,method:str):
    endpoint = "/search/"
    url = f"{API_URL}{endpoint}"
    params = {
        "query": text,
        "method": method
    }
    r = requests.get(url, params=params)
    df = (
        pd.json_normalize(r.json()["res"])
    )
    return df[['person_name','count','wa']]

starter_query="graph databases"
starter_method="full"
df  = search(text=starter_query,method=starter_method)

def layout_function():
    return html.Div([
        dcc.Input(id='input-1-state', type='text', value=starter_query),
        dcc.Input(id='input-2-state', type='text', value=starter_method),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        html.Div(id='output-state'),
        #generate_table(df)
        dash_table.DataTable(
            id='table',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            #editable=True,
            #filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            #row_selectable="multi",
            row_deletable=False,
            #selected_columns=[],
            #selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])

app.layout = layout_function

@app.callback(Output('table', 'data'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'),
              State("table","data")
              )
def run_search(n_clicks, input1, input2, table_data):
    df = search(text=input1,method=input2)
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)