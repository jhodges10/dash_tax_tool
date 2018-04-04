import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dlib import masternode_tax_calc


app = dash.Dash()

# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

app.layout = html.Div([
    html.H4('TaxTable - initial load is slow'),
    dcc.Input(
        placeholder='Insert Dash Address... ',
        size=40,
        id='address',
        value='XxVpWcsE92qWTrZWfmGTqrCzpBaKhRf2tX',
        type='text'),

    dcc.Graph(
        id='tax-graph',
    ),

    dt.DataTable(
        # Initialise the rows
        rows=[{}],
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='table'
    ),

    html.Div(id='tax-calc'),
], className='container')

# Table and data from input field
@app.callback(
    Output('table', 'rows'),
    [Input(component_id='address', component_property='value')])
def get_data_object(address):
    cost_basis = masternode_tax_calc.generate_cost_basis(address)
    df = pd.DataFrame.from_records(cost_basis)
    """
    For user selections, return the relevant in-memory data frame.
    """
    df = df.to_dict('records')
    return df

# Graphing
@app.callback(
    Output('tax-graph', 'figure'),
    [Input('table', 'rows')])
def update_figure(rows):
    dff = pd.DataFrame(rows)
    figure = {
        'data': [
            {'x': dff.date, 'y': dff.cost_basis, 'type': 'bar', 'name': "Dash MN Count"},
        ],
        'layout': {
            'title': "Cost Basis"
        }
    }
    return figure

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)