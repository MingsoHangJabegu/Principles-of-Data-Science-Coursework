from dash import Dash, dcc, html

from pages.house_prices_page import get_layout as get_house_prices_layout, register_callbacks as register_house_callbacks
from pages.council_tax_page import get_layout as get_council_tax_layout, register_callbacks as register_council_callbacks
from pages.broadband_page import get_layout as get_broadband_layout, register_callbacks as register_broadband_callbacks
from pages.visualisation_page import get_layout as get_visualisation_layout, register_callbacks as register_visualisation_callbacks

app = Dash(__name__)
app.title = 'Data Dashboard'

app.layout = html.Div([
    html.Div([
        html.H1('Simple Data Dashboard', style={'marginBottom': '0.5rem', 'color': '#1f2a44', 'fontSize': '2.4rem'}),
        html.P('Explore house prices, council tax, broadband performance, and interactive visualisations.', style={'marginTop': '0', 'color': '#495867', 'fontSize': '1rem'}),
        dcc.Tabs(id='tabs', value='tab-house', children=[
            dcc.Tab(label='House Prices', value='tab-house', children=[get_house_prices_layout()]),
            dcc.Tab(label='Broadband', value='tab-broadband', children=[get_broadband_layout()]),
            dcc.Tab(label='Council Tax', value='tab-council', children=[get_council_tax_layout()]),
            dcc.Tab(label='Visualisation', value='tab-visualisation', children=[get_visualisation_layout()]),
        ], style={'fontWeight': '600'}, content_style={'padding': '1rem'}),
    ], style={'maxWidth': '1400px', 'margin': '0 auto'}),
], style={'padding': '2rem', 'backgroundColor': '#f5f7fb', 'minHeight': '100vh'})

register_house_callbacks(app)
register_council_callbacks(app)
register_broadband_callbacks(app)
register_visualisation_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
