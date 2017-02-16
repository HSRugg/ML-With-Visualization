from bokeh.models.widgets import Select, Slider
from bokeh.layouts import row, gridplot, widgetbox
from bokeh.charts import Bar
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Range1d #TickFormatter, LinearColorMapper, Plot, Range1d, LinearAxis, FixedTicker, FuncTickFormatter
from bokeh.plotting import figure, output_file, show
# from bokeh.models.widgets import Slider
from bokeh.io import show
from bokeh.models.ranges import FactorRange
import numpy as np
import pickle
import pandas as pd
import get_some_data as gsd


books = pickle.load( open( "authos_books_df_clean.p", "rb" ) )
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

# Create a new plot with a title and axis labels
plot = figure(title="Important Words With TRIDF", x_axis_label='Parts of Speach',
	 		  y_axis_label='TRIDF Score',x_range=source.data['pos_types'])


#add an image
# plot.image_url(url=['a_new_hope.png'], x=0, y=1, w=3, h=3)


# add plot and set style
plot.rect('x', 'y_offset',.35, 'height',source=source)
plot.title.text_color = "blue"
plot.title.text_font = "times"
plot.title.align = "center"
plot.title.text_font_size = "22pt"

plot.y_range.start = 0
plot.xaxis.major_label_orientation = 3.14/4
    
    
def update_dropdown(attrname, old, new):
	print type(author_dropdown.value), author_dropdown.value
	title_dropdown.options = ['None'] + [metadata[book]['title'] for book in books[author_dropdown.value]]
	
	
	
def update_data(attrname, old, new):
	
	# print my_dropdown.value.encode('utf-8')
	# print type(my_dropdown.value.encode('utf-8'))
	# print titles['A Set of Six']
	# print type(titles['A Set of Six'])
	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	book_id = str(book_id)
	print "getting data for:", title_dropdown.value, 'Id:', book_id
	source.data, words = gsd.get_Tridf_data(book_id,n_gram_slider.value)
	plot.x_range.factors = words
	# plot.y_range.bounds = (0, None)
	current_auther = author_dropdown.value
	plot.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'


def update_n_grams(attr, old, new):
	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	book_id = str(book_id)
	print "getting data for:", title_dropdown.value, 'Id:', book_id
	source.data, words = gsd.get_Tridf_data(book_id,n_gram_slider.value)
	plot.x_range.factors = words
	current_auther = author_dropdown.value
	plot.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'


# Add some widgets     
n_gram_slider = Slider(start=1, end=10, title='Number of words', step=1, value=1)
n_gram_slider.on_change('value', update_n_grams)

author_dropdown = Select(title='Author', value='None', options=['None'] + books.index.values.tolist())
author_dropdown.on_change('value', update_dropdown)

title_dropdown = Select(title='Book', value='None', options=['None'])
title_dropdown.on_change('value', update_data)

wb = widgetbox([author_dropdown,title_dropdown,n_gram_slider])

grid = gridplot([[wb],[plot]], toolbar_location=None)
curdoc().add_root(grid)


