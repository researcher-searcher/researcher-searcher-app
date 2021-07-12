import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Researcher Searcher - Bristol Medical School (PHS)"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Search", href="search")),
        dbc.NavItem(dbc.NavLink("Person", href="person")),
        dbc.NavItem(dbc.NavLink("Collaboration", href="collaboration")),
        dbc.NavItem(dbc.NavLink("About", href="about")),
        dbc.NavItem(dbc.NavLink("API", href="https://rs-phs-api.mrcieu.ac.uk")),
    ],
    brand="Researcher Searcher - Bristol Medical School (PHS)",
    brand_href="/",
    color="primary",
    dark=True,
)

footer = dbc.NavbarSimple(color="primary", dark=True,)

server = app.server
app.config.suppress_callback_exceptions = True
