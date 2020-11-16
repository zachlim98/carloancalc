import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("True Cost of Car (with Interest and Monthly Expenses)", style={'text-align':'center'}),
    html.Hr(),
    html.P("This calculator allows you to estimate the true cost of your car (over 10 years), taking into account loan downpayment, loan term, interest rates, and estimated monthly expenses (on fuel, parking etc.).", style={'text-align':'center'}),
    html.Div([
    dcc.Input(
        id='carprice',
        min=50000,
        value='',
        placeholder="Retail Price",
        type="number",
        style={'text-align':'center'}
    ),
    dcc.Input(
        id='monthexp',
        min=500,
        value='',
        placeholder="Monthly Expenses",
        type="number",
        style={'text-align':'center'}
    )], style=dict(display='flex', justifyContent='center')),
    html.Div([
        dcc.Input(
        id='intrate',
        min=0.01,
        value='',
        placeholder="Interest Rates (%)",
        type="number",
        style={'text-align':'center'}
    )], style=dict(display='flex', justifyContent='center')),
    html.Hr(),
    dcc.Graph(id='graph-car-price')
])


@app.callback(
    Output('graph-car-price', 'figure'),
    [Input('carprice', 'value'),
    Input('monthexp','value'),
    Input('intrate','value'),
    ])
def update_figure(carprice, monthexp, intrate):
    downpayment_list = [i for i in range(int(carprice*0.3),int(carprice),200)]
    # create dataframe
    car_loan_df = pd.DataFrame({"Downpayment" : downpayment_list
                                })

    # add total cost of car to dataframe
    for z in range(1,8):
        car_loan_df["{} Year".format(z)] = [(((intrate/100)*z*(carprice - downpayment_list[i])+(carprice - downpayment_list[i])))+downpayment_list[i]+monthexp for i in range(0,len(downpayment_list))]

    # melt for easier plotting
    car_melt = pd.melt(car_loan_df, id_vars="Downpayment")

    fig = px.line(car_melt,x="Downpayment",y="value",color="variable",labels={
                        "Downpayment": "Initial Downpayment",
                        "value": "Total Cost of Car",
                        "variable": "Loan Term"
                    }, color_discrete_sequence=px.colors.qualitative.Bold)

    fig.update_layout({"plot_bgcolor":"white"})
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)