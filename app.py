# import things
import os
from flask import Flask, render_template
from dlib import masternode_tax_calc

app = Flask(__name__)

# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
    {
        "field": "type",  # which is the field's name of data key
        "title": "Tx Type",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "amount",
        "title": "Tx Size",
        "sortable": True,
    },
    {
        "field": "cost_basis",
        "title": "Cost Basis",
        "sortable": True,
    },
    {
        "field": "date",
        "title": "Tx Date",
        "sortable": True,
    },
]


@app.route('/')
def index():
    tax_info = masternode_tax_calc.generate_cost_basis()
    data = tax_info
    return render_template("table.html", data=data, columns=columns, title='Dash Tax Tool')


if __name__ == '__main__':
    port_config = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port_config)
