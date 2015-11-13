from __future__ import division
from __future__ import print_function
from collections import Counter

from nltk.tree import *
from nltk.draw import tree

from nltk.corpus import brown

from nltk.util import ngrams
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.data import load

from nltk import CFG

from nltk import Tree

import nltk

import json

tagdict = load('help/tagsets/brown_tagset.pickle')

#taglist = tagdict.keys()

#taglist stored in the file
f = open('concise_taglist','r')
tagLine = f.readline().rstrip('\n')
tagLine = tagLine.split(',')
tagDict = set()
for i in range(0,tagLine.__len__()):
	tagDict.add(tagLine[i].strip())
taglist = list(tagDict)
taglist.remove('NP')
taglist.remove('')
taglist = ['NP']+taglist
f.close()

taglist_size = taglist.__len__()

tag_sequence_corpus = brown.tagged_sents(tagset='brown')

tag_list = []
corpus_with_tag = []
#Everything is tagged, including the punctuations and the lines
print("Creating tag lists....")
for sentences in tag_sequence_corpus:
	for tags in sentences:
		word = tags[0]
		wordTag = tags[1]
		if '+' in wordTag:
			position = wordTag.find('+')
			wordTag = wordTag[0:position]		
		if '-' in wordTag and wordTag!='--':
			position = wordTag.find('-')
			wordTag = wordTag[0:position]
		tag_list.append(wordTag)
		corpus_with_tag.append((word,wordTag))

print("Done creating tag lists....")

print("Creating tag corpus...")
#Code snippet that works upon the unigrams list
unigrams = ngrams(tag_list,1)
unigrams_freq = Counter(unigrams);

#Code snippet that works upon the bigrams list
bigrams = ngrams(tag_list,2)
bigrams_freq = Counter(bigrams);

#Code snippet that works upon the trigrams list
trigrams = ngrams(tag_list,3)
trigrams_freq = Counter(trigrams);

#Length of the corpus
len_corpus = brown.words().__len__()

word_with_tag = Counter(corpus_with_tag)
print("Corpus tagged!")

def S(k):
	"This function returns the set value S for the viterbi algorithm"
	if k in (-1,0): return [""]
	else: return taglist 

def argmax(ls):
	return max(ls, key = lambda x:x[1])

def trigramCounter(w,u,v):
	ans = 0.0 if bigrams_freq[(u,v,)] == 0 else float(trigrams_freq[(w,u,v)])/float(bigrams_freq[(u,v,)])
	ans += 0.0 if unigrams_freq[(u,)] == 0 else float(bigrams_freq[(u,v,)])/float(unigrams_freq[(u,)])
	ans += float(unigrams_freq[(v,)])/float(len_corpus)
	ans = ans/3;
	return ans

def q(v,w,u):
	"This function returns the trigram count estimation"
	return trigramCounter(w,u,v)	

def e(x,u):
	w_t = word_with_tag[(x,u,)]
	t = unigrams_freq[(u,)]
	if t == 0 : t = 1
	return w_t/t 
		

def Viterbi(sentence):
	"This function implements the viterbi algorithm for a given function"
	#The pi refers to the dictionary for the Viterbi tagset probabilties	
	pi = {}
	#Initialization
	pi[0,"",""] = 1.0
	#This array, called as backpointer is used to retrieve the tags corresponding to a given sentence
	bp = {}
	#Tokens converts the sentence into array of words and punctuations
	tokens = word_tokenize(sentence)
	n = tokens.__len__()
	#Padding so that the sentence begins at the position 1
	tokens = [""]+tokens
	#The viterbi algorithm
	for k in range(1,n+1):
		for u in S(k-1):
			for v in S(k):
				bp[k,u,v], pi[k,u,v] = argmax([(w, pi[k-1,w,u]* q(v,w,u) * e(tokens[k],v)) for w in S(k-2)])
	#Now the dictionary pi consists of the maximum probabilities of tag sequences
	#We first create an array of n+1 length to store all the tags
	y = [""]*(n+1)
	(y[n-1],y[n]),score = argmax([( (u,v), pi[n,u,v]*q(".",u,v) ) for u in S(n-1) for v in S(n)])

	for k in range(n-2,0,-1):
		y[k] = bp[k+2, y[k+1],y[k+2]]
	y[0]=""
	return y

def cutit(s,rem,n):
	n = n + rem.__len__()
	return s[n:]

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

def dict_to_json(dict):
    return json.dumps(dict)

def main():
	while 1 == 1 :
		print("Enter a statement")
		statement = raw_input()
		statement = statement.lower()


		tagged_arr = Viterbi(statement)

		#check if all of the elements are same
		count = 1
		tag = tagged_arr[1]
		for i in range(2,tagged_arr.__len__()):
			if tagged_arr[i] == tag:
				count = count + 1
		
		if count == tagged_arr.__len__()-1:
			tokens = word_tokenize(statement)
			n = tokens.__len__()
			for i in range(0,n):
				tag_temp = Viterbi(tokens[i])[1]
				tagged_arr[i+1] = tag_temp
				if tokens[i]=='open':
					tagged_arr[i+1] = 'VB'
				if tokens[i]=='file':
					tagged_arr[i+1] = 'NN'
					
				

		print(tagged_arr)
		
		simple_grammar = CFG.fromstring("""
		  S -> NP VP
		  S -> VP
		  NP -> MODAL PRON | DET NP | NOUN VF | NOUN
 		  MODAL -> 'MD'
      		  PRON -> 'PPSS' | 'PPO'
 		  VP -> VERB NP
		  VP -> VERB VP
		  VP -> ADVERB VP
		  VP -> VF
	          VERB -> 'VB' | 'VBN'
		  NOUN -> 'NN' | 'NP'
 		  VF -> VERB FILENAME
  		  FILENAME -> 'NN' | 'NP'
		  ADVERB -> 'RB'
	          DET -> 'AT'
		  """)

		tagged_arr.remove('')
		parser = nltk.ChartParser(simple_grammar)

		json = ''

		for tree in parser.parse(tagged_arr):
			#print(tree)
			#tree.draw()
			json = dict_to_json(tree2dict(tree))
		
		print(json)

main()
