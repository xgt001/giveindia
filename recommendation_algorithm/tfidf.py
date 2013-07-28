#!/usr/bin/env python

# a = [st.stem(w)  for w in word_list if not w in stopwords.words('english') and wordnet.synsets(st.stem(w)) and wordnet.synsets(w)]
__author__ = "Arpan Gupta"
__email__ = "arpangupta420 at gmail dot com"

import math
import re
from collections import Counter
from operator import itemgetter
import nltk
import nltk.data
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import movie_reviews
_debug = 1

class TfIdf:

	#either reads from the already generated corpus or populates a corpus from a given file
	#can be updated further to have 
	def __init__(self, **other_vars):
		
		self.st = LancasterStemmer()
		self.sd = nltk.data.load('tokenizers/punkt/english.pickle')
		self.num_words = 0 #In the corpus, no of words excluding the stopwords
		self.term_freq = {} #In the corpus, term : number of terms 
		self.stop_words = [ stopword.strip() for stopword in stopwords.words('stopwords') ] #reuters english keywords
		self.idf_default = other_vars.get('DEFAULT_IDF', 1.5)
		self.corpus_filename = other_vars.get('corpus_filename')
		self.summary = {}
		if self.corpus_filename :
			#if corpus file is given, read from it else leave as it is right now
			corpus_file = open(self.corpus_filename, 'r')
			#the first line will denote #words
			self.num_words = int(corpus_file.readline().strip())
			#now populate the words from the corpus, i/p in the form of 'terms:count of that term' while 	
			for line in corpus_file:
				token = line.rpartition(':') # a 3-tuple is returned 
				self.term_freq[token[0].strip()] = int(token[2].strip())
		elif _debug:
			print "No input file"

				 
	def add_document_to_corpus(self, filename = None):
		if filename:
			inp_file = open(filename,'r')
		else:
			inp_file = movie_reviews.raw()
   		words = self.get_tokens(inp_file)
		words_freq = Counter(words)
		self.num_words += len(words_freq)
 		for word in words_freq:
      			if word in self.term_freq:
        			self.term_freq[word] += words_freq[word]
      			else:
        			self.term_freq[word] = words_freq[word]			

	def get_tokens(self, file):
		symbols = r'~`!@#$%^&*()-_+={}[]|\:;",<>,.?/ \\ \' \ '
		lines = ''
		for line in file:
			lines+=line
		lines = re.sub('[\d]+','',lines)		
		#tokenize, remove stop words, stem

		raw_tokens = [word.strip(str(symbols)) for word in wordpunct_tokenize(lines.lower()) if not  word in symbols and not word in self.stop_words and not word.strip(str(symbols)) == ""]
		tokens = []	
		'''	 #not working properly
		for token in raw_tokens:
			if wordnet.synsets(token):
				if wordnet.synsets(self.st.stem(token)):
					tokens.append(self.st.stem(token))
			else: tokens.append(token)
		'''	
		
		return raw_tokens
		 
	def save_corpus_to_file(self, idf_filename):

		output_file = open(idf_filename, "w")
		output_file.write(str(self.num_words) + "\n")
		for term, num in self.term_freq.items():
			output_file.write(term + ": " + str(num) + "\n")			

	def get_idf(self, term):
		if term in self.stop_words:
			return 0
		elif not term in self.term_freq:
			return self.idf_default
		else:
			return math.log(float(1 + self.num_words) /  (1 + self.term_freq[term]) )


	def get_doc_keywords(self, inp_filename):
		file = open(inp_filename, 'r')
		tfidf = {}
		tokens = self.get_tokens(file)
		tokens_dic = Counter(tokens)
		for token in tokens_dic:
			tf = float(tokens_dic[token])/ len(tokens) #text frequency
			idf = self.get_idf(token) #inverse document frequency wrt to the corpus
			tfidf[token] = tf * idf 
		return sorted(tfidf.items(), key=itemgetter(1), reverse=True)

	def get_summary(self, inp_filename, no_lines):
		doc_keywords = dict(self.get_doc_keywords(inp_filename))
		score_dict = {}
		lines = ''
		file = open(inp_filename, 'r')
		for line in file:
			lines+=line		
		sentences =	self.sd.tokenize(lines.strip(), realign_boundaries=True)
		for sentence in sentences:
			score = 0
			tokens = self.get_tokens(sentence)
			for token in tokens:
				score += doc_keywords[token]
			score_dict[sentence] = score
		
		return sorted(score_dict.items(), key=itemgetter(1), reverse=True)[:no_lines]				
				

