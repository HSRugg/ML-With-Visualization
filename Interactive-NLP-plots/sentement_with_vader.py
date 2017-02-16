from bokeh.plotting import figure, output_file, show
from bokeh.layouts import widgetbox, gridplot
from bokeh.models.widgets import Slider, Select
from scipy.signal import butter, lfilter, freqz
from nltk.tokenize import sent_tokenize, word_tokenize
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bokeh.models import ColumnDataSource
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
source = ColumnDataSource(data=dict(
	x = range(0,len(butter_lowpass_filter(compound,cutoff,fs))),
	y = butter_lowpass_filter(compound,cutoff,fs)
    ))


# Create figer, fiter data and add data to figuer as 'patch' plot
p = figure(plot_width=900, plot_height=300,title='Compound Sentiment')
p.patch(x='x', y='y',source=source, color="#11a8a1")


# Add fs silder function and slider 
def update_fs(attr, old, new):
    source.data = dict(
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
	source.data = dict(
	x = range(0,len(butter_lowpass_filter(compound,cutoff,fs_slider.value))),
	y = butter_lowpass_filter(compound,cutoff,fs_slider.value))


author_dropdown = Select(title='Author', value='None', options=['None'] + books.index.values.tolist())
author_dropdown.on_change('value', update_dropdown)

title_dropdown = Select(title='Book', value='None', options=['None'])
title_dropdown.on_change('value', update_data)


# wb_menus = widgetbox([author_dropdown,title_dropdown])

#set up layout and send to current doc.
wb = widgetbox([author_dropdown,title_dropdown,fs_slider])
grid = gridplot([[wb],[p]], toolbar_location=None)
curdoc().add_root(grid)


