import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
from dlib import masternode_tax_calc
import os
from json import JSONDecodeError


app = dash.Dash()

# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True

app.layout = html.Div([
    html.H4('Calculate Dash Taxes!'),
    html.H6('Sometimes it does crash... Working on adding features.'),

    html.Br(),
    html.Br(),

    html.H5('Enter Dash address below'),

    html.Div([
        dcc.Input(
            id='address',
            placeholder='XxVpWcsE92qWTrZWfmGTqrCzpBaKhRf2tX',
            value='',
            size=40,
            type='text',
            pattern='^X[1-9A-HJ-NP-Za-km-z]{33}'
        )],
        className='address-bar'
    ),

    html.Button('Calculate', id='calc-but', n_clicks=0),

    dcc.Graph(
        id='tax-graph',
    ),

    html.Br(),

    dt.DataTable(
        # Initialise the rows
        rows=[{}],
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='tx_table'
    ),

    html.Br(),
    html.Br(),

], className='container')


@app.callback(
    Output('tx_table', 'rows'),
    [Input('calc-but', 'n_clicks')], [State('address', 'value')])
def get_address_info(n_clicks, value):
    try:
        cost_basis = masternode_tax_calc.generate_cost_basis(value)
    except JSONDecodeError:
        cost_basis = {
            'amount': 0,
            'time': 15223753709,
            'date': '2018-01-01',
            'type': 'normal',
            'cost_basis': '0',
        }
    df = pd.DataFrame.from_records(cost_basis).sort_values(by=['date'], ascending=False)
    """
    For user selections, return the relevant in-memory data frame.
    """
    df = df.to_dict('records')
    return df


@app.callback(
    Output('tax-graph', 'figure'),
    [Input('tx_table', 'rows')])
def update_figure(rows):
    dff = pd.DataFrame(rows)
    figure = {
        'data': [
            {'x': dff.date, 'y': dff.cost_basis, 'type': 'line', 'name': "Dash Tax Cost Basis"},
        ],
        'layout': {
            'title': "Cost Basis"
        }
    }
    return figure


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

'''
dcc._css_dist[0]['relative_package_path'].append('dash-tax.css')


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
'''


if __name__ == '__main__':
    port_config = int(os.getenv('PORT', 5000))
    app.run_server(host='0.0.0.0', port=port_config, debug=True)
