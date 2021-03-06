from __future__ import division
from collections import Counter

from nltk.corpus import brown
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer

#Code to read the sentence from the file
file = open('test.txt','r')
sentence = file.read();
sentence_broke = sent_tokenize(sentence)

#Thoe following code snippets work in the following fashion
#Line 1 refers to an array that stores the count of the n-grams
#Line 2 refers to the brown corpus broken into n-grams
#Line 3 calculates the frequency of the ngrams in corpus

#Code snippet that works upon the unigrams list
unigrams = ngrams(brown.words(),1)
unigrams_freq = Counter(unigrams);

#Code snippet that works upon the bigrams list
bigrams = ngrams(brown.words(),2)
bigrams_freq = Counter(bigrams);

#Code snippet that works upon the trigrams list
trigrams = ngrams(brown.words(),3)
trigrams_freq = Counter(trigrams);

len_corpus = brown.words().__len__()

for sentence in sentence_broke:
	tokened = RegexpTokenizer(r'\w+')
	tokened = tokened.tokenize(sentence)
	unigram_set = ngrams(tokened,1)
	bigram_set = ngrams(tokened,2)
	trigram_set = ngrams(tokened,3)
	w2 = "*"
	w1 = "*"
	uni_q = []
	bi_q = []
	tri_q = []
	bi_q.append(1.0)
	tri_q.append(1.0)
	tri_q.append(1.0)
	ans = 0.0
	q_trigram_count = 1.0
	lambda1 = 1.0/3.0
	lambda2 = 1.0/3.0
	lambda3 = 1.0/3.0
	for words in unigram_set:
		uni_q.append(unigrams_freq[words])
	for words in bigram_set:
		bi_q.append(bigrams_freq[words])
	for words in trigram_set:
		tri_q.append(trigrams_freq[words])

	for i in range(2,tokened.__len__()):
		ans = 0.0 if bi_q[i-1] == 0 else float(tri_q[i])/float(bi_q[i-1])
		ans += 0.0 if uni_q[i-1] == 0 else float(bi_q[i])/float(uni_q[i-1])
		ans += float(uni_q[i])/float(len_corpus)
		ans = ans/3;
		q_trigram_count *= ans

	#q_trigram_count now has the product of all the probabilities in it
	print(sentence,q_trigram_count)

