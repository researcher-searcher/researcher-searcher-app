import dash
import dash_bootstrap_components as dbc

from environs import Env

env = Env()
env.read_env()

TITLE=env.str("TITLE")
API=env.str("API_URL")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = TITLE

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Search", href="search")),
        dbc.NavItem(dbc.NavLink("Person", href="person")),
        dbc.NavItem(dbc.NavLink("Collaboration", href="collaboration")),
        dbc.NavItem(dbc.NavLink("About", href="about")),
        dbc.NavItem(dbc.NavLink("API", href=API)),
    ],
    brand=f"Researcher Searcher - {TITLE}",
    brand_href="/",
    color="primary",
    dark=True,
)

footer = dbc.NavbarSimple(color="primary", dark=True,)

server = app.server
app.config.suppress_callback_exceptions = True
