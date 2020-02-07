import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

healthy_df = pd.read_csv('all_ages_healthy_app_params.csv')
diseased_df = pd.read_csv('all_ages_perthes_app_params.csv')

param_names = healthy_df.columns[3:]
ages = healthy_df['Age'].unique()
# Param types: 'shape', 'app' or 'tex'
param_type = 'app'

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in param_names],
                placeholder="Select an x-axis " + param_type + " parameter",
                value=(param_type + '_param_1')
            )
        ],
                style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in param_names],
                placeholder="Select a y-axis " + param_type + " parameter",
                value=(param_type + '_param_2')
            )
        ],
                style={'width': '48%', 'float': 'right',
                       'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='age_selection',
                options=[{'label': i, 'value': i} for i in ages],
                placeholder="Select an age",
                value=2
            )
        ],
                style={'width': '48%', 'float': 'bottom',
                       'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('age_selection', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, age_selection):
    healthy_dff = healthy_df[healthy_df['Age'] == age_selection]
    diseased_dff = diseased_df[diseased_df['Age'] == age_selection]
    return {
        'data': [dict(x=healthy_dff[xaxis_column_name],
                      y=healthy_dff[yaxis_column_name],
                      text=healthy_dff['Disease'],
                      mode='markers',
                      marker={'size': 15, 'opacity': 0.5,
                              'line': {'width': 0.5, 'color': 'white'}},
                      name='Healthy'),
                 dict(x=diseased_dff[xaxis_column_name],
                      y=diseased_dff[yaxis_column_name],
                      text=diseased_dff['Disease'],
                      mode='markers',
                      marker={'size': 15, 'opacity': 0.5,
                              'line': {'width': 0.5, 'color': 'red'}},
                      name='Diseased')
                 ],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
