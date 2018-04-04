import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dlib import masternode_tax_calc
import pandas as pd

cost_basis = masternode_tax_calc.generate_cost_basis()
df = pd.DataFrame.from_records(cost_basis)

def generate_table(dataframe, max_rows=20):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),

    html.H1(children='Dash Address Tax Info'),
    generate_table(df),
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)