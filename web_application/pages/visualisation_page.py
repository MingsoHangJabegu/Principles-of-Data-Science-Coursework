from dash import dcc, html, Input, Output
from web_application.query.visualisation import house_prices_visualisation
from web_application.query.connection import run_query


def load_oxford_wards():
    df = run_query("SELECT ward_name " \
    "FROM ward w JOIN local_authority l " \
    "ON w.local_authority_code = l.local_authority_code " \
    "WHERE l.local_authority_name = 'Oxford' " \
    "ORDER BY ward_name")
    return [{'label': name, 'value': name} for name in df['ward_name'].tolist()]


def load_cherwell_wards():
    df = run_query("SELECT ward_name " \
    "FROM ward w JOIN local_authority l " \
    "ON w.local_authority_code = l.local_authority_code " \
    "WHERE l.local_authority_name = 'Cherwell' " \
    "ORDER BY ward_name")
    return [{'label': name, 'value': name} for name in df['ward_name'].tolist()]


oxford_wards_options = load_oxford_wards()
cherwell_wards_options = load_cherwell_wards()


def get_layout():
    section_style = {
        'backgroundColor': '#ffffff',
        'border': '1px solid #e3e6ea',
        'borderRadius': '14px',
        'padding': '1.5rem',
        'boxShadow': '0 8px 20px rgba(0, 0, 0, 0.04)',
        'marginBottom': '1.5rem',
    }
    filter_row = {
        'display': 'flex',
        'flexWrap': 'nowrap',
        'alignItems': 'flex-end',
        'gap': '1%',
        'overflowX': 'auto',
        'paddingBottom': '0.5rem',
    }
    field_style = {
        'flex': '1 1 24%',
        'minWidth': '220px',
        'display': 'flex',
        'flexDirection': 'column',
    }

    return html.Div([
        html.Div([
            html.Div([
                html.Label('Select up to 5 Oxford Wards', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                dcc.Dropdown(
                    id='oxford-wards',
                    options=oxford_wards_options,
                    value=['Barton and Sandhills', 'Blackbird Leys', 'Carfax', 'Churchill', 'Cowley'],
                    multi=True,
                    style={'minWidth': '0'},
                ),
            ], style=field_style),
            html.Div([
                html.Label('Select up to 5 Cherwell Wards', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                dcc.Dropdown(
                    id='cherwell-wards',
                    options=cherwell_wards_options,
                    value=['Adderbury, Bloxham and Bodicote', 'Banbury Calthorpe and Easington', 'Banbury Cross and Neithrop', 'Banbury Grimsbury and Hightown', 'Banbury Hardwick'],
                    multi=True,
                    style={'minWidth': '0'},
                ),
            ], style=field_style),
            html.Div([
                html.Label('Start Year', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                dcc.Dropdown(
                    id='vis-start-year',
                    options=[{'label': str(year), 'value': str(year)} for year in range(2013, 2024)],
                    value='2013',
                    clearable=False,
                    style={'minWidth': '0'},
                ),
            ], style=field_style),
            html.Div([
                html.Label('End Year', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                dcc.Dropdown(
                    id='vis-end-year',
                    options=[{'label': str(year), 'value': str(year)} for year in range(2013, 2024)],
                    value='2023',
                    clearable=False,
                    style={'minWidth': '0'},
                ),
            ], style=field_style),
        ], style=filter_row),
        html.Div([
            dcc.Graph(id='house-price-trends'),
        ], style=section_style),
        html.Div([
            dcc.Graph(id='house-price-comparison'),
        ], style=section_style),
    ], style={'fontFamily': 'Arial, sans-serif', 'color': '#23374d'})


def register_callbacks(app):
    @app.callback(
        Output('oxford-wards', 'value'),
        Input('oxford-wards', 'value')
    )
    def limit_oxford_wards(value):
        if value and len(value) > 5:
            return value[:5]
        return value

    @app.callback(
        Output('cherwell-wards', 'value'),
        Input('cherwell-wards', 'value')
    )
    def limit_cherwell_wards(value):
        if value and len(value) > 5:
            return value[:5]
        return value

    @app.callback(
        Output('house-price-trends', 'figure'),
        Output('house-price-comparison', 'figure'),
        Input('oxford-wards', 'value'),
        Input('cherwell-wards', 'value'),
        Input('vis-start-year', 'value'),
        Input('vis-end-year', 'value'),
    )
    def update_visualisation(oxford_wards, cherwell_wards, start_year, end_year):
        selected_wards = oxford_wards + cherwell_wards
        fig1, fig2 = house_prices_visualisation(selected_wards, start_year, end_year)
        if fig1 is None:
            fig1 = {}
        if fig2 is None:
            fig2 = {}
        return fig1, fig2