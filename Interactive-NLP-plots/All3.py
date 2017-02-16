from bokeh.plotting import figure, output_file, show
from bokeh.layouts import widgetbox, gridplot
from bokeh.models.widgets import Slider, Select
from scipy.signal import butter, lfilter, freqz
from nltk.tokenize import sent_tokenize, word_tokenize
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bokeh.models import ColumnDataSource
import get_some_data as gsd
from bokeh.io import curdoc
import pandas as pd
import pickle

#unpicle metatdata
books = pickle.load( open( "authos_books_df_clean.p", "rb" ) )
metadata = pickle.load( open( "gutenberg_metadata.p"  , "rb" ) )

# get compound sentiment data by book id
def get_compound_sentiment(text_id):
	# brake into sentences ans then analyze sentiment
	text = strip_headers(load_etext(text_id)).strip()
	sentences = sent_tokenize(text)
	sid = SentimentIntensityAnalyzer()
	neg, neu, pos, compound = [],[],[],[]
	for sentence in sentences[0:]:
	    #print(sentence)
	    ss = sid.polarity_scores(sentence)
	    neg.append(ss['neu'])
	    neu.append(ss['neu'])
	    pos.append(ss['pos'])
	    compound.append(ss['compound'])
	return compound , len(sentences)

compound, sentence_count = get_compound_sentiment(2021)

# Create fiters
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5): 
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    # add an addition zero to the end to hold the plot areas in shape.
    y = y.ravel().tolist()
    y.insert(len(y)+1,0)
    return y

# Filter requirements.
order = 6
fs = 30       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz


#Create ColumnDataSource for interaction
source_sen = ColumnDataSource(data=dict(
	x = range(0,len(butter_lowpass_filter(compound,cutoff,fs))),
	y = butter_lowpass_filter(compound,cutoff,fs)
    ))

# prepare some data
x = [1, 2, 3, 4, 5]
height = [6, 7, 2, 4, 5]
width = .35


source3 = ColumnDataSource(data=dict(x = x,
									height = height,
									y_offset = [y*0.5 for y in height],
									pos_types = ['a','b','c','d','e']))


source = ColumnDataSource(data=dict(x = x,
									height = height,
									y_offset = [y*0.5 for y in height],
									pos_types = ['a','b','c','d','e']))

# Create figer, fiter data and add data to figuer as 'patch' plot
p = figure(plot_width=900, plot_height=300,title='Compound Sentiment')
p.patch(x='x', y='y',source=source_sen, color="#11a8a1")


# Add fs silder function and slider 
def update_fs(attr, old, new):
    source_sen.data = dict(
	x = range(0,len(butter_lowpass_filter(compound,cutoff,fs_slider.value))),
	y = butter_lowpass_filter(compound,cutoff,fs_slider.value))
    
fs_slider = Slider(start=30, end=sentence_count, step=100, value=30,
 title='FS for Nouse Filter; Incress to View Treadns')
fs_slider.on_change('value', update_fs)


# Add author and book selectors functions and dropdowns.
def update_dropdown(attrname, old, new):
	print type(author_dropdown.value), author_dropdown.value
	title_dropdown.options = ['None'] + [metadata[book]['title'] for book in books[author_dropdown.value]]
	
	
def update_data(attrname, old, new):

	# get a list of titles and get the book id, pass to get sentiment function
	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	compound, sentence_count = get_compound_sentiment(book_id)
	fs_slider.end = sentence_count
	# update plot data
	cutoff = 3.667
	source_sen.data = dict(
	x = range(0,len(butter_lowpass_filter(compound,cutoff,fs_slider.value))),
	y = butter_lowpass_filter(compound,cutoff,fs_slider.value))

	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	book_id = str(book_id)
	source.data, pos_tags = gsd.get_pos_data(book_id)
	plot2.x_range.factors = pos_tags
	# plot.y_range.bounds = (0, None)
	current_auther = author_dropdown.value
	plot2.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	
	source3.data, words = gsd.get_Tridf_data(book_id,n_gram_slider.value)
	plot3.x_range.factors = words
	plot3.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'

	


author_dropdown = Select(title='Author', value='None', options=['None'] + books.index.values.tolist())
author_dropdown.on_change('value', update_dropdown)

title_dropdown = Select(title='Book', value='None', options=['None'])
title_dropdown.on_change('value', update_data)
# current_auther = 'Conrad, Joseph'
# titles = {metadata[book]['title'] : book for book in books[current_auther]}


# create a new plot with a title and axis labels
plot2 = figure(title="Frequencys for Parts of Speach", x_axis_label='Parts of Speach',
	 		  y_axis_label='Frequency',x_range=source.data['pos_types'])


# add plot and set style
plot2.rect('x', 'y_offset',.35, 'height',source=source)
plot2.title.text_color = "blue"
plot2.title.text_font = "times"
plot2.title.align = "center"
plot2.title.text_font_size = "22pt"
plot2.y_range.start = 0
plot2.xaxis.major_label_orientation = 3.14/4
	
    

# Create a new plot with a title and axis labels
plot3 = figure(title="Important Words With TRIDF", x_axis_label='Parts of Speach',
	 		  y_axis_label='TRIDF Score',x_range=source.data['pos_types'])


#add an image
# plot.image_url(url=['a_new_hope.png'], x=0, y=1, w=3, h=3)


# add plot and set style
plot3.rect('x', 'y_offset',.35, 'height',source=source)
plot3.title.text_color = "blue"
plot3.title.text_font = "times"
plot3.title.align = "center"
plot3.title.text_font_size = "22pt"

plot3.y_range.start = 0
plot3.xaxis.major_label_orientation = 3.14/4
    
    
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
	source3.data, words = gsd.get_Tridf_data(book_id,n_gram_slider.value)
	plot3.x_range.factors = words
	# plot.y_range.bounds = (0, None)
	current_auther = author_dropdown.value
	plot3.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'


def update_n_grams(attr, old, new):
	titles  = {metadata[book]['title'] : book for book in books[author_dropdown.value]}
	book_id = titles[title_dropdown.value.encode('utf-8')]
	book_id = str(book_id)
	source3.data, words = gsd.get_Tridf_data(book_id,n_gram_slider.value)
	plot3.x_range.factors = words
	current_auther = author_dropdown.value
	plot3.title.text = title_dropdown.value.encode('utf-8') +\
	" By " + current_auther.split(", ")[1]+" " +current_auther.split(",")[0]
	print 'done'


# Add some widgets     
n_gram_slider = Slider(start=1, end=10, title='Number of words', step=1, value=1)
n_gram_slider.on_change('value', update_n_grams)



#set up layout and send to current doc.
wb = widgetbox([author_dropdown,title_dropdown,fs_slider])
grid = gridplot([[wb],[p],[plot2, plot3,widgetbox(n_gram_slider)]], toolbar_location=None)
curdoc().add_root(grid)


