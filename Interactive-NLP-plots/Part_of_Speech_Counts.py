from bokeh.models.widgets import Select
from bokeh.layouts import row, gridplot
from bokeh.charts import Bar
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Range1d #TickFormatter, LinearColorMapper, Plot, Range1d, LinearAxis, FixedTicker, FuncTickFormatter
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import widgetbox
# from bokeh.models.widgets import Slider
from bokeh.io import output_notebook, push_notebook, show
from bokeh.models.ranges import FactorRange
import numpy as np
import pickle
import pandas as pd
import get_some_data as gsd




books = pickle.load( open( "authos_books_df_full.p", "rb" ) )
metadata = pickle.load( open( "gutenberg_metadata.p"  , "rb" ) )

current_auther = 'Conrad, Joseph'
titles = {metadata[book]['title'] : book for book in books[current_auther]}


# prepare some data
x = [1, 2, 3, 4, 5]
height = [6, 7, 2, 4, 5]
width = .35


source = ColumnDataSource(data=dict(x = x,
									height = height,
									y_offset = [y*0.5 for y in height],
									pos_types = ['a','b','c','d','e']))

# create a new plot with a title and axis labels
plot = figure(title="Frequencys for Parts of Speach", x_axis_label='Parts of Speach',
	 		  y_axis_label='Frequency',x_range=source.data['pos_types'])


# add plot and set style
plot.rect('x', 'y_offset',.35, 'height',source=source)
plot.title.text_color = "blue"
plot.title.text_font = "times"
plot.title.align = "center"
plot.title.text_font_size = "22pt"

plot.y_range.start = 0
plot.xaxis.major_label_orientation = 3.14/4

# align, background_fill_alpha, background_fill_color, border_line_alpha, 
# border_line_cap, border_line_color, border_line_dash, border_line_dash_offset, 
# border_line_join, border_line_width, js_callbacks, level, name, offset, plot, 
# render_mode, tags, text, text_alpha, text_color, text_font, text_font_size, 
# text_font_style or visible
# plot.text([.5, 2.5], [.5, .5], text=['Yes', 'No'],
#                    text_font_size="20pt", text_align='center')
# plot.xaxis.visible = None
# plot.xgrid.grid_line_color = None

# show the results

	
	
    
    
def update_dropdown(attrname, old, new):
	print type(author_dropdown.value), author_dropdown.value
	title_dropdown.options = ['None'] + [metadata[book]['title'] for book in books[author_dropdown.value]]
	
	
	
def update_data(attrname, old, new):
	print title_dropdown.value
	print 'check one!'
	# print my_dropdown.value.encode('utf-8')
	# print type(my_dropdown.value.encode('utf-8'))
	# print titles['A Set of Six']
	# print type(titles['A Set of Six'])
	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	book_id = str(book_id)
	print book_id
	source.data, pos_tags = gsd.get_data(book_id)
	plot.x_range.factors = pos_tags
	# plot.y_range.bounds = (0, None)
	current_auther = author_dropdown.value
	plot.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'

author_dropdown = Select(title='Author', value='None', options=['None'] + books.index.values.tolist())
author_dropdown.on_change('value', update_dropdown)

title_dropdown = Select(title='Book', value='None', options=['None'])
title_dropdown.on_change('value', update_data)


wb = widgetbox([author_dropdown,title_dropdown])



# for selector in selectors:
#     selector.on_change('value', input_change)
grid = gridplot([[wb],[plot]], toolbar_location=None)
curdoc().add_root(grid)


