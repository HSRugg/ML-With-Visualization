from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from collections import Counter
import pandas as pd
import numpy as np
import make_image_clowd as mic

def get_pos_data(data_to_get):
	print 'happedn 1:', data_to_get
	heights = get_pos_counts(int(data_to_get))
	print heights
	pos_types = [pos_dict[h.upper()] for h in heights.index.values.tolist()]

	return dict(			x 			= range(1,13,1),
							height 		= heights.values,
							y_offset 	= [h*0.5 for h in heights.values],
							pos_types   = ['a','f','g','d','e','a','f','g','d','e','l','k']
							), pos_types
	
									
	
# nostromo = strip_headers(load_etext(2021)).strip()
# typhoon = strip_headers(load_etext(1142)).strip()
# Under_Western_Eyes = strip_headers(load_etext(2480)).strip()

def get_pos_counts(book_id):
	book_text = strip_headers(load_etext(book_id)).strip()
	pos = [pos for word, pos in nltk.pos_tag(word_tokenize(book_text))]
	pos_counts = pd.Series(pos).value_counts().head(12)
	print len(pos_counts)
	return pos_counts



pos_dict = {
'PRP$'  : 'Possessive pronoun',
'VBG'	: 'Verb, gerund/present participle',
'FW'	: 'Foreign word',
'VBN'	: 'Verb, past participle',
'VBP'	: 'Verb, sing. present, non-3d',
'WDT'	: 'Wh-determiner',
'JJ'	: 'Adjective',
'WP'	: 'Wh-pronoun',
'VBZ'	: 'Verb, 3rd person sing. present',
'DT'	: 'Determiner',
'RP'	: 'Particle',
'NN'	: "Noun, singular 'desk'",
'VBD'	: 'Verb, past tense',
'POS'	: 'Possessive ending',
'TO'	: 'To',
'PRP'	: 'Personal pronoun',
'RB'	: 'Adverb',
'NNS'	: 'Noun plural',
'NNP'	: 'Proper noun, singular',
'VB'	: 'Verb, base form',
'WRB'	: 'Wh-abverb',
'CC'	: 'Coordinating conjunction',
'LS'	: 'List marker',
'PDT'	: 'Predeterminer',
'RBS'	: 'Adverb, superlative',
'RBR'	: 'Adverb, comparative',
'CD'	: 'Cardinal digit',
'EX'	: 'Existential there (like: "there is" ... think of it like "there exists")',
'IN'	: 'Preposition/subordinating conjunction',
'WP$'	: 'Possessive wh-pronoun',
'MD'	: 'Modal',
'NNPS'	: 'Proper noun, plural',
'JJS'	: 'Adjective, superlative',
'JJR'	: 'Adjective, comparative',
'UH'	: 'Interjection',
'.'		: 'Periods',
','		: 'Commas'}



def get_Tridf_data(book_id, n_grams=1):
	book_text = strip_headers(load_etext(int(book_id))).strip()
	#Use the TfidfVectorizer to find important ngrams 
	vect = TfidfVectorizer(stop_words='english',ngram_range=(n_grams,n_grams))

	# Pulls all of trumps tweet text's into one giant string
	# summaries = "".join(trump_df['text'])
	ngrams_summaries = vect.build_analyzer()(book_text)
	words =  np.array(Counter(ngrams_summaries).most_common(12))[0:,0:1]
	heights = np.array(Counter(ngrams_summaries).most_common(12))[0:,1:2]
	df = pd.DataFrame(np.hstack((words,heights)), columns=['words','counts'])
	mic.make_image_from_text(int(book_id))
	
	# pos_types = [pos_dict[h.upper()] for h in heights.index.values.tolist()]

	return dict(			x 			= range(1,13,1),
							height 		= df['counts'].values.tolist(),
							y_offset 	= [int(h)*.5 for h in df['counts'].values],
						pos_types   = ['a','f','g','d','e','a','f','g','d','e','l','k']
						), df['words'].values.tolist()

