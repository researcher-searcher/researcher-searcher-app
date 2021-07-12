import dash_core_components as dcc
import dash
import dash_html_components as html
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
    Output("person-table", "data"),
    Output("person-loading-output-1", "children"),
    Input("person-submit-button-state", "n_clicks"),
    Input("person-submit-button-state", "value"),
    State("person-input-1-state", "value"),
)
def run_person(n_clicks, value, input1):
    if n_clicks == 0:
        return dash.no_update
    else:
        df = api_person(text=input1)
        return df.to_dict("records"), value


# callback for collab page
@app.callback(
    Output("collab-table", "data"),
    # Output('collab-plot', 'figure'),
    Output("collab-loading-output-1", "children"),
    Input("collab-submit-button-state", "n_clicks"),
    Input("collab-submit-button-state", "value"),
    State("collab-input-1-state", "value"),
    State("collab-input-2-state", "value"),
)
def run_collab(n_clicks, value, input1, input2):
    if n_clicks == 0:
        return dash.no_update
    else:
        df = api_collab(text=input1, method=input2)
        return df.to_dict("records"), value


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
