from dash import dcc, html, Input, Output, dash_table
from database.council_tax_queries import get_council_tax_data
from database.xml_queries import xml_council_tax
from database.connection import run_query


def load_council_tax_areas():
    df = run_query("SELECT DISTINCT area_name FROM council_tax_area ORDER BY area_name")
    return [{'label': name, 'value': name} for name in df['area_name'].tolist()]


band_options = [{'label': b, 'value': b} for b in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']]

council_tax_areas = load_council_tax_areas()
TABLE_STYLE = {
    'overflowX': 'auto',
    'minWidth': '100%',
}
TABLE_STYLE_CELL = {
    'textAlign': 'left',
    'padding': '12px',
    'whiteSpace': 'normal',
    'height': 'auto',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'fontSize': '14px',
    'color': '#34495e',
    'border': '1px solid #e3e6ea',
}
TABLE_STYLE_HEADER = {
    'backgroundColor': '#f5f7fb',
    'fontWeight': '700',
    'border': '1px solid #e3e6ea',
    'borderBottom': '2px solid #e3e6ea',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'fontSize': '14px',
    'color': '#1f2a44',
}


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
        'flexWrap': 'wrap',
        'alignItems': 'flex-end',
        'gap': '1rem',
        'overflowX': 'auto',
        'paddingBottom': '0.5rem',
    }
    field_style = {
        'flex': '0 0 auto',
        'width': '260px',
        'minWidth': '180px',
        'maxWidth': '320px',
        'display': 'flex',
        'flexDirection': 'column',
    }

    return html.Div([
        html.Div([
            html.H4('Town comparison filters', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Town 1', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='council-town-1',
                        options=council_tax_areas,
                        value=council_tax_areas[0]['value'] if council_tax_areas else None,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
                html.Div([
                    html.Label('Town 2', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='council-town-2',
                        options=council_tax_areas,
                        value=(
                            council_tax_areas[1]['value']
                            if len(council_tax_areas) > 1
                            else (council_tax_areas[0]['value'] if council_tax_areas else None)
                        ),
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style=field_style),
            ], style=filter_row),
        ], style={**section_style, 'marginBottom': '0.75rem'}),
        html.Div([
            html.H4('Tax Difference', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            dash_table.DataTable(
                id='council-tax-diff-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
                style_as_list_view=False,
            ),
        ], style=section_style),
        html.Div([
            html.H4('Lowest Band B Charge', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            dash_table.DataTable(
                id='council-lowest-tax-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
                style_as_list_view=False,
            ),
        ], style=section_style),
        html.Div([
            html.H4('Band selection filters', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.Div([
                html.Div([
                    html.Label('Select up to 3 bands', style={'fontWeight': '600', 'marginBottom': '0.5rem'}),
                    dcc.Dropdown(
                        id='council-bands',
                        options=band_options,
                        value=['A', 'B', 'C'],
                        multi=True,
                        clearable=False,
                        style={'width': '100%'},
                    ),
                ], style={**field_style, 'flex': '1 1 28%'}),
            ], style={**filter_row, 'marginBottom': '1rem', 'gap': '2%'}),
            html.H4('Highest Band C Charge', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            html.P(id='xml-council-tax-summary', style={'margin': '0', 'fontSize': '1rem', 'fontWeight': '600', 'color': '#34495e', 'marginBottom': '1rem'}),
            html.H4('Average Council Tax for Selected Bands', style={'marginBottom': '0.75rem', 'color': '#1f2a44'}),
            dash_table.DataTable(
                id='xml-council-tax-table',
                page_size=10,
                style_table=TABLE_STYLE,
                style_cell=TABLE_STYLE_CELL,
                style_header=TABLE_STYLE_HEADER,
                style_as_list_view=False,
            ),
        ], style=section_style),
    ], style={'fontFamily': 'Arial, sans-serif', 'color': '#23374d'})


def register_callbacks(app):
    @app.callback(
        Output('council-bands', 'value'),
        Input('council-bands', 'value')
    )
    def limit_bands(value):
        if value and len(value) > 3:
            return value[:3]
        return value

    @app.callback(
        Output('council-tax-diff-table', 'data'),
        Output('council-tax-diff-table', 'columns'),
        Output('council-lowest-tax-table', 'data'),
        Output('council-lowest-tax-table', 'columns'),
        Output('xml-council-tax-table', 'data'),
        Output('xml-council-tax-table', 'columns'),
        Output('xml-council-tax-summary', 'children'),
        Input('council-town-1', 'value'),
        Input('council-town-2', 'value'),
        Input('council-bands', 'value'),
    )
    def update_council_tax(town_1, town_2, bands):
        tax_diff, lowest_tax = get_council_tax_data(town_1, town_2)
        tax_diff = tax_diff.copy()
        tax_diff['Charge_1'] = tax_diff['Charge_1'].astype(float).map('{:.2f}'.format)
        tax_diff['Charge_2'] = tax_diff['Charge_2'].astype(float).map('{:.2f}'.format)
        tax_diff['Tax_Difference'] = tax_diff['Tax_Difference'].astype(float).map('{:.2f}'.format)
        diff_data = tax_diff.to_dict('records')
        diff_columns = [
            {'name': 'Town 1', 'id': 'Area_1'},
            {'name': 'Town 1 Charge (£)', 'id': 'Charge_1'},
            {'name': 'Town 2', 'id': 'Area_2'},
            {'name': 'Town 2 Charge (£)', 'id': 'Charge_2'},
            {'name': 'Tax Difference (£)', 'id': 'Tax_Difference'},
        ]
        lowest_tax = lowest_tax.copy()
        lowest_tax['Lowest_Tax'] = lowest_tax['Lowest_Tax'].astype(float).map('{:.2f}'.format)
        lowest_data = lowest_tax.to_dict('records')
        lowest_columns = [
            {'name': 'Town', 'id': 'Town'},
            {'name': 'Lowest Band B Charge (£)', 'id': 'Lowest_Tax'},
        ]

        selected_bands = bands or ['A', 'B', 'C']
        if isinstance(selected_bands, str):
            selected_bands = [selected_bands]
        selected_bands = [band.upper() for band in selected_bands][:3]
        if not selected_bands:
            selected_bands = ['A', 'B', 'C']

        area_averages, max_row = xml_council_tax(selected_bands)
        xml_df = area_averages.reset_index()
        xml_df.columns = ['area', 'average_amount']
        xml_df['average_amount'] = xml_df['average_amount'].astype(float).map('{:.2f}'.format)
        xml_data = xml_df.to_dict('records')
        xml_columns = [
            {'name': 'Area', 'id': 'area'},
            {'name': 'Average Amount (£)', 'id': 'average_amount'},
        ]
        summary = (
            f"{max_row['area']} has the highest Band C charge with £{max_row['amount']:.2f}."
        )

        return diff_data, diff_columns, lowest_data, lowest_columns, xml_data, xml_columns, summary
