import dash
import dash_core_components as dcc
import dash_html_components as html
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

components = [Population(), Location(), FlockKMeans(), Infection()]
sim = setup_simulation(components)
pop = sim.get_population()


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

dcc.Graph(id='boid-plot',
          figure={'data': plot_boids(pop),
          'layout': {'xaxis': {'range': [0, 1000], 'autorange': False},
                     'yaxis': {'range': [0, 1000], 'autorange': False},
                     'title': 'Start Title',
                     'updatemenus': [{'type': 'buttons',
                                      'buttons': [{'label': 'Play',
                                                   'method': 'animate',
                                                   'args': [None]}]}]
                    },

            # 'frames': frames,

         }
),

])


if __name__ == '__main__':
    app.run_server(debug=True)