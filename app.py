import dash
import dash_bootstrap_components as dbc

#app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])
app.title = 'Researcher Searcher'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Search", href="search")),
        dbc.NavItem(dbc.NavLink("Person", href="person")),
        dbc.NavItem(dbc.NavLink("Collaboration", href="collaboration")),
        dbc.NavItem(dbc.NavLink("About", href="about")),
    ],
    brand="Researcher Searcher - UoB Data Science Network",
    brand_href="/",
    color="primary",
    dark=True,
)

server = app.server
app.config.suppress_callback_exceptions = True
