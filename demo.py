import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
port = 8881

# Specifying the app layout
app.layout = html.Div([
    html.H1("Hello Dash!!!"),
    html.Div("Dash - GUI"),


    dcc.Graph(
        id='SampleChart',
        figure={
            'data': [
                {'x': [4, 6, 8], 'y':[12, 16, 18],
                    'type':'bar', 'name':'First Chart'},
                {'x': [4, 6, 8], 'y':[10, 24, 26],
                    'type':'bar', 'name':'First Chart'}
            ],
            'layout': {
                'title': 'Simple Bar Chart'
            }
        }
    )
])


if __name__ == '__main__':
    app.run_server(port=port)
