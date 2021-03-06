from dash import dcc, html, callback_context
import dash
import plotly.express as px
import time
from dash.dependencies import Input, Output, State
from apps.search import api_search
from functions import (
    api_search,
    api_search_person,
    api_search_output,
    api_person,
    api_collab,
    api_lookup,
    run_tsne,
)
from app import app, server
from apps import home, search, person, collaboration, about
from loguru import logger

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    logger.info(pathname)
    if pathname == "/search":
        return search.layout
    elif pathname == "/person":
        return person.layout
    elif pathname == "/collaboration":
        return collaboration.layout
    elif pathname == "/about":
        return about.layout
    else:
        return home.layout


# callback for search page
@app.callback(
    Output("search-table", "data"),
    Output("search-table", "columns"),
    Output("search-fig", "figure"),
    Output("search-fig", "style"),
    Output("search-slider", "style"),
    Output("search-loading-output-1", "children"),
    # Output('search-table', 'tooltip_data'),
    Input("search-submit-button-state", "n_clicks"),
    Input("search-slider", "value"),
    Input("search-submit-button-state", "value"),
    State("search-input-1-state", "value"),
    State("search-input-2-state", "value"),
)
def run_search(n_clicks, slider_val, value, input1, input2):
    logger.info(slider_val)
    if n_clicks == 0 and slider_val == 50:
        return dash.no_update
    else:
        logger.info("Recreating plot...")
        fig = {}
        fig_style = {"display": "none"}
        slider_style = {"display": "none"}
        logger.info(f"{input1} {input2}")
        if input2 in ["full", "vec", "combine"]:
            df = api_search(text=input1, method=input2).head(n=slider_val)
            # xy plot
            fig = px.scatter(
                df.head(n=slider_val),
                x="WA",
                y="Top Score",
                hover_data=["Name"],
                size="Count",
                color="Org",
                symbol="Org",
                labels={"WA": "Weighted Average (WA)",},
                title=f"Top {slider_val} people",
            )
            fig_style = {"height": "60vh"}
            slider_style = {"display": "block"}
        elif input2 == "person":
            df = api_search_person(text=input1)
        elif input2 == "output":
            df = api_search_output(text=input1)
        columns = [{"name": i, "id": i} for i in df.columns]
        # logger.debug(columns)

        # tooltip
        # tooltip_data = [{c:{'type': 'text', 'value': f'{r},{c}'} for c in df.columns} for r in df[df.columns].values]
        # tooltip_data= [   {
        #                        column: {'value': str(value), 'type': 'markdown'}
        #                            for column, value in row.items()
        #                        } for row in df.to_dict('records')
        #                    ],
        # logger.debug(tooltip_data)
        return df.to_dict("records"), columns, fig, fig_style, slider_style, value


# callback for person page
@app.callback(
    Output('list-suggested-inputs', 'children'),
    Output("person-table", "data"),
    Input("person-submit-button-state", "n_clicks"),
    Input({"id": 'dest-loc', "type": "searchData"}, "value"),
    prevent_initial_call=True
)
def run_person(n_clicks, value):
    # if submit button not pressed, run the autocomplete
    global lookup_data
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]

    #f n_clicks == 0:
    if 'person-submit-button-state' in changed_id:
        person_id = lookup_data[value]
        df = api_person(text=person_id)
        return [], df.to_dict("records")  
    else:
        if len(value) < 3:
            raise dash.exceptions.PreventUpdate
        else:
            df_lookup = api_lookup(text=value)
            try:
                lookup_names = df_lookup['person_name'].values()
                lookup_ids = df_lookup['pid'].values()
                lookup_data = dict(zip(lookup_names, lookup_ids))
                person_list = list(df_lookup['person_name'].values())
                return [html.Option(value=l) for l in person_list], []
            except:
                return [], []


# callback for collab page
@app.callback(
    #Output('collab-list-suggested-inputs', 'children'),
    #Output("collab-table", "data"),
    #Output("collab-loading-output-1", "children"),
    #Input("collab-submit-button-state", "n_clicks"),
    #Input("collab-submit-button-state", "value"),
    #State("collab-input-1-state", "value"),
    #State("collab-input-2-state", "value"),

    Output('collab-list-suggested-inputs', 'children'),
    Output("collab-table", "data"),
    Input("collab-submit-button-state", "n_clicks"),
    Input({"id": 'collab-input-1-state', "type": "searchData"}, "value"),
    State("collab-input-2-state", "value"),
    prevent_initial_call=True
)
def run_collab(n_clicks, input1, input2):
    # if submit button not pressed, run the autocomplete
    global lookup_data
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'collab-submit-button-state' in changed_id:
        person_id = lookup_data[input1]
        df = api_collab(text=person_id, method=input2)
        return [], df.to_dict("records")
    else:
        if len(input1) < 3:
            raise dash.exceptions.PreventUpdate
        else:
            df_lookup = api_lookup(text=input1)
            lookup_names = df_lookup['person_name'].values()
            lookup_ids = df_lookup['pid'].values()
            lookup_data = dict(zip(lookup_names, lookup_ids))
            person_list = list(df_lookup['person_name'].values())
            return [html.Option(value=l) for l in person_list], []

# callback for home page
# @app.callback(Output('home-fig', 'figure'),
#              Input('home-submit-button-state', 'n_clicks'),
#              State('home-input-1-state', 'value'),
#              )
# def update_plot(n_clicks, input1):
#    fig = run_tsne(query=input1)
#    return fig

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
