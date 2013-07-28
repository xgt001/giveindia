from tfidf import TfIdf

def main():
	tfidf = TfIdf(corpus_filename = "moviecorpus.txt")
#	tfidf.add_document_to_corpus()
#	print tfidf.term_freq
#	print tfidf.num_words
	for line in tfidf.get_summary('oblivion.txt', 5):
		print line
#	print tfidf.get_idf('create')
#	print tfidf.get_doc_keywords('man_of_steel.txt')
#	tfidf.save_corpus_to_file('moviecorpus.txt')	
if __name__ == "__main__" : main()
