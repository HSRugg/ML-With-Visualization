
''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc, show, output_notebook
from bokeh.layouts import row, widgetbox, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Select, Panel, RadioButtonGroup
from bokeh.plotting import figure
from sklearn.datasets import make_biclusters, make_blobs, make_circles, make_moons
from sklearn.cluster import SpectralClustering
import pandas as pd


# Set up data
df, blob_y = make_blobs(n_samples=400, n_features=3, centers=4, cluster_std=1.4)
#make_circles(n_samples=100, shuffle=True, noise=None, random_state=None, factor=0.8)


def map_colors(groups_list):
    new_group_list_as_color = []
    for group in groups_list:
        if group == 0:
            new_group_list_as_color.append('green')
        elif group == 1:
            new_group_list_as_color.append('blue')
        elif group == 2:
            new_group_list_as_color.append('green')
        elif group == 3:
            new_group_list_as_color.append('yellow')
        elif group == 4:
            new_group_list_as_color.append('black')
        elif group == 5:
            new_group_list_as_color.append('pink')
        elif group == 6:
            new_group_list_as_color.append('orange')
        elif group == 7:
            new_group_list_as_color.append('red')
    return new_group_list_as_color

def update_data(attrname, old, new):
    
    # Get the current slider values
    nn  = n_neighbors.value
    cl = n_clusters.value
    mi = max_iter.value
    if radio_button_group.active   == 0:
        affinity = "nearest_neighbors"
    elif radio_button_group.active == 1:
        affinity = "precomputed"
    elif radio_button_group.active == 2:
        affinity =  "rbf"
    print radio_button_group.active
    #alg = algorithm.value

    sc = SpectralClustering(n_clusters=cl, n_neighbors=nn,affinity=affinity)
    pred_types = sc.fit_predict(df)
    pred_types = map_colors(pred_types)

    source.data['type'] = pred_types


sc = SpectralClustering(n_clusters=4)
pred_types = sc.fit_predict(df)
# km = KMeans(n_init=10, max_iter=300, n_clusters=4)
# pred_types = km.fit_predict(df)
pred_types = map_colors(pred_types)

df = pd.DataFrame(df,columns=['x','y','a'])

source = ColumnDataSource(data=dict(x = df['x'].values,
                                    y = df['y'].values,
                                    a = df['a'].values,
                                    type = pred_types))

# Set up plot

plot_kmean = figure(plot_height=400, plot_width=400,
 title="Spectral Clustering Unsupervised Model", tools="")
plot_kmean.circle('x', 'y', source=source, size=4, color='type')
plot_kmean.xaxis.axis_label = 'X - Var'
plot_kmean.yaxis.axis_label = 'Y - Var'
            


plot_kmean2 = figure(plot_height=400, plot_width=400,
 title="Spectral Clustering Unsupervised Model", tools="crosshair,pan,reset,save,wheel_zoom")
plot_kmean2.circle('a', 'y', source=source, size=4, color='type')
plot_kmean2.xaxis.axis_label = 'A - Var'
plot_kmean2.yaxis.axis_label = 'Y - Var'
    

plot_kmean3 = figure(plot_height=400, plot_width=400,
 title="Spectral Clustering Unsupervised Model", tools="crosshair,pan,reset,save,wheel_zoom")
plot_kmean3.circle('x', 'a', source=source, size=4, color='type')
plot_kmean3.xaxis.axis_label = 'X - Var'
plot_kmean3.yaxis.axis_label = 'A - Var'
    


# Set up widgets
# text = TextInput(title="title", value='my sine wave')
# offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
n_neighbors     = Slider(title="n_neighbors", value=10, start=1.0, end=40.0, step=1)
n_clusters      = Slider(title="n_clusters", value=4, start=1, end=7, step=1)
max_iter        = Slider(title="max_iter", value=300, start=10, end=900, step=1)
# p = Slider(title="p", value=0.5, start=0.1, end=.9)



def my_radio_handler(new):
    # Get the current slider values
    nn  = n_neighbors.value
    cl = n_clusters.value
    mi = max_iter.value
    if radio_button_group.active   == 0:
        affinity = "nearest_neighbors"
    elif radio_button_group.active == 1:
        affinity = "precomputed"
    elif radio_button_group.active == 2:
        affinity =  "rbf"
    print radio_button_group.active
    #alg = algorithm.value

    sc = SpectralClustering(n_clusters=cl, n_neighbors=nn,affinity=affinity)
    pred_types = sc.fit_predict(df)
    pred_types = map_colors(pred_types)

    source.data['type'] = pred_types


radio_button_group = RadioButtonGroup(
        labels=["nearest_neighbors", "precomputed", "rbf"], active=0)


# Set up callbacks
for w in [n_neighbors,n_clusters,max_iter]:
    w.on_change('value', update_data)

radio_button_group.on_click(my_radio_handler)



# Set up layouts and add to document




inputs_kmean = widgetbox([n_neighbors,n_clusters,max_iter,radio_button_group])

grid = gridplot([[plot_kmean, plot_kmean2], [plot_kmean3, inputs_kmean]], toolbar_location=None)
curdoc().add_root(grid)
curdoc().title = "Spectral Clustering"





