# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

from environs import Env

env = Env()
env.read_env()

TITLE=env.str("TITLE")
API=env.str("API_NAME")

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
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
        ), 
    ])

    return layout
