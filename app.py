import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from vivarium.interface import setup_simulation
from src.population import Population
from src.location import Location
from src.flock import FlockKMeans
from src.infection import Infection

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = '''
# Hello Vivarium
'''

# components = [Population(), Location(), FlockKMeans(), Infection()]
# sim = setup_simulation(components)
# pop = sim.get_population()


def run_simulation(n_steps, n_clusters=5):
    components = [Population(), Location(), FlockKMeans(), Infection()]
    sim = setup_simulation(components)

    # Set parameters
    sim.configuration.flock.n_clusters = n_clusters

    pop = sim.get_population()
    pop['color'] = pop.infected.map({0: 'black', 1: 'red'})
    pops = [sim.get_population()]
    for i in range(0, n_steps):
        sim.step()
        pop = sim.get_population()
        pop['color'] = pop.infected.map({0: 'black', 1: 'red'})
        pops.append(pop)

    return pops

def plot_boids(pop):
    return [go.Scatter(x=pop.x,
                y=pop.y,
                text=pop.infected,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 5,
                    'color': pop.color,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='Boids')]

app.layout = html.Div([

# HEADER
 dcc.Markdown(children=top_markdown_text),
html.P('Number of steps'),
        dcc.Slider(
            id='n-steps',
            min=5,
            max=10,
            step=1,
            marks={i: str(i) for i in range(5, 10 + 1)},
            value=5,
        ),
html.P('Number of clusters'),
        dcc.Slider(
            id='n-clusters',
            min=2,
            max=8,
            step=1,
            marks={i: str(i) for i in range(2, 8 + 1)},
            value=7,
        ),
dcc.Graph(id='boid-plot', animate=True),

])

@app.callback(Output('boid-plot', 'figure'),
              [Input('n-steps', 'value')])
def run_boid_simulation(n_steps):
    pops = run_simulation(n_steps)
    print(len(pops))
    frames = [{'data': plot_boids(pops[i])} for i in range(1, len(pops))]

    return {'data': plot_boids(pops[0]),
          'layout': {'xaxis': {'range': [0, 1000], 'autorange': False},
                     'yaxis': {'range': [0, 1000], 'autorange': False},
                     'title': 'Start Title',
                     'updatemenus': [{'type': 'buttons',
                                      'buttons': [{'label': 'Play',
                                                   'method': 'animate',
                                                   'args': [None]}]}]
                    },

            'frames': frames,

         }




if __name__ == '__main__':
    app.run_server(debug=True)
