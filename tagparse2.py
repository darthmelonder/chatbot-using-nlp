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

import os

import action
from action import *

import filecheck
from filecheck import *

tagdict = load('help/tagsets/brown_tagset.pickle')

#taglist = tagdict.keys()

#taglist stored in the file
f = open('concise_taglist','r')
tagLine = f.readline().rstrip('\n')
tagLine = tagLine.split(',')
tagDict = set()
for i in range(0,len(tagLine)):
	tagDict.add(tagLine[i].strip())
taglist = list(tagDict)
taglist.remove('NP')
taglist.remove('')
taglist = ['NP']+taglist
taglist = ['AN']+taglist
f.close()

appnames = []
commands = []

verbList = ['copy','open','close','exit','shut','move','make','create','cut','change']

#os.system("./app.awk")

userName = ''

f = open('appnames.txt','r')
for line in f:
	if '=>' in line:
		line_chunks = line.split('=>')
		n = len(line_chunks)
		for i in range(0,n-1):
			an = line_chunks[i].strip().lower()
			if 'disk' not in an:
				appnames.append(line_chunks[i].strip().lower())
				command = line_chunks[n-1].rstrip('\n')
				if '%' in command:
					position = command.find('%')
					command = command[0:position]
				commands.append(command.strip())
#os.system('rm appnames.txt')

f.close()

def userNameLoader():
	os.system('whoami>myname')
	f = open('myname','r')
	user = ''
	for line in f:
		userName = line.rstrip('\n')
	f.close()
	os.system('rm myname')

taglist_size = len(taglist)

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
	n = n + len(rem)
	return s[n:]

def tree2dict(tree):
    return {tree.label(): [tree2dict(t)  if isinstance(t, Tree) else t
                        for t in tree]}

def dict_to_json(dict):
    return json.dumps(dict)

def tree2json(tree):
	return json.loads(dict_to_json(tree2dict(tree)))

def main():
	while 1 == 1 :

		print("Enter a statement")
		statement = raw_input().strip()
		if statement == '':
			continue
		if statement in ['bye','goodbye','tata','good-bye']:
			print("Good-bye, dear human")
			exit()
		userNameLoader() #loads the username

		tagged_arr = Viterbi(statement)

		tokens = word_tokenize(statement)

		isFile = False
		isDir = False

		#check if all of the elements are same
		count = 1
		tag = tagged_arr[1]
		for i in range(2,len(tagged_arr)):
			if tagged_arr[i] == tag:
				count = count + 1
		
		if count == len(tagged_arr)-1:
			n = len(tokens)
			for i in range(0,n):				
				tag_temp = Viterbi(tokens[i])[1]
				tagged_arr[i+1] = tag_temp

		for i in range(0,len(tokens)):
			if i+2 <= len(tokens):
				if tokens[i] in ['folder','file','directory'] and tagged_arr[i+2] in ['VB','VBN']:
					tagged_arr[i+1] = 'NN'
			elif tokens[i] in ['folder','file','directory'] and tagged_arr[i] in ['VB','VBN']:
					tagged_arr[i+1]='NN'

		for i in range (0,len(tokens)):
			if tagged_arr[i+1] in ['NN','NNS','NP','VB','AN','JJ'] and tokens[i]!= 'open':
				for j in range(0,len(appnames)):
					if tokens[i].lower() in appnames[j] and tokens[i].lower() not in ['file','folder','directory','copy','videos','desktop']:
						tagged_arr[i+1]='AN'
						tokens[i] = commands[j]
						isFile = True
						break
				if isDirName(userName,tokens[i])==True:
						tagged_arr[i+1] = 'AN'
						isDir = True
				elif isFileName(userName,tokens[i])==True:
						tagged_arr[i+1] = 'AN'
						isFile = True

		for i in range (0,len(tokens)):
			if tokens[i] in verbList:
				tagged_arr[i+1] = 'VB'
		
		print(tagged_arr)

		grammar_string = """
		  S -> NP VP
		  S -> VP
		  NP -> MODAL PRONOUN | NOUN VA | APPNAME
		  NP -> DET FOLDER VERB NAME | FOLDER VERB NAME| FOLDER NAME | DET NAME
		  NP -> DET APPNAME
		  NP -> BACK TONAME | DET BACK TONAME
		  NP -> WQUERY
		  WQUERY -> WQL AP NOUN | WRB AP NOUN
		  BACK -> 'background' | 'BACKGROUND' | 'Background'
		  BACK -> 'wallpaper' | 'WALLPAPER' | 'Wallpaper'
		  BACK -> AN
		  TONAME -> TO FILENAME | TO DET FILENAME
		  CPY -> DET FILENAME SOURCE DESTINATION | DET FILENAME DESTINATION SOURCE
		  CPY -> FILENAME SOURCE DESTINATION | FILENAME DESTINATION SOURCE
		  SOURCE -> IN SOURCER
	     	  SOURCER -> DET FOLDER VBN APPNAME | DET FOLDER APPNAME | DET APPNAME
		  SOURCER -> FOLDER VBN APPNAME | FOLDER APPNAME | APPNAME
		  DESTINATION -> TO DESTINATIONR
		  DESTINATIONR -> DET FOLDER VBN APPNAME | DET FOLDER APPNAME | DET APPNAME 
		  DESTINATIONR -> FOLDER VBN APPNAME | FOLDER APPNAME | APPNAME
		  FOLDER -> 'folder'|'directory'|'file'|'Folder'|'File'|'Directory'|'FOLDER'|'FILE'|'DIRECTORY'
		  FOLDER -> NN
		  VP -> VERB NP | VERB VP | ADVERB VP | VERB CPY
		  VP -> BER RB IN PPS
		  PPS -> DET PP | PP
		  PP -> JJ NOUN | NOUN | FOLDER VBN DET FILENAME | FOLDER VBN FILENAME | FOLDER FILENAME | FOLDER DET FILENAME 
		  PP -> FILENAME
		  MODAL -> MD
		  PRONOUN -> PPSS | PPO
		  VA -> VERB APPNAME
                  APPNAME -> AN
  		  VERB -> VB | VBN
		  ADVERB -> RB
		  DET -> AT
		  NOUN -> NN | NNS
		  FILENAME -> AN
		  """
		
		str = 'NAME -> '
		for i in range(1,len(tagged_arr)):
			str+=tagged_arr[i]
			if i < len(tagged_arr)-1:
				str+=" | "

		str+="\n"

		grammar_string += str

		#add POS tags
		tl = len(tagged_arr)
		for i in range(1,tl):
			if tokens[i-1] not in ['file','folder','directory']:
				grammar_string+=tagged_arr[i]+" -> \'"+tokens[i-1]+"\'\n"

		simple_grammar = CFG.fromstring(grammar_string)

		parser = nltk.ChartParser(simple_grammar)

		json_str = ''
	
		ANs= []
		ANJSON = []
		VBs = []
		VBJSON = []
		NAMEs= []
		NJSON = []
		CCYs = []
		SOURCEs = []
		DESTs = []
		FILENAMEs = []
		TONAMEs = []
		TONAMEFILEs = []

		for tree in parser.parse(tokens):
			print(tree)
			ANs = list(tree.subtrees(filter=lambda x: x.label()=='AN'))
			VBs = list(tree.subtrees(filter=lambda x: x.label()=='VERB'))
			NAMEs = list(tree.subtrees(filter=lambda x: x.label()=='NAME'))
			CCYs = list(tree.subtrees(filter=lambda x:x.label()=='CCY'))
			SOURCEs = list(tree.subtrees(filter=lambda x:x.label()=='SOURCER'))
			SOURCEs = map(lambda x: list(x.subtrees(filter=lambda x: x.label()=='AN')), SOURCEs)
			DESTs = list(tree.subtrees(filter = lambda x:x.label()=='DESTINATIONR'))
			DESTs = map(lambda x: list(x.subtrees(filter=lambda x: x.label()=='AN')), DESTs)
			FILENAMEs = list(tree.subtrees(filter = lambda x:x.label()=='FILENAME'))
			FILENAMEs = map(lambda x: list(x.subtrees(filter=lambda x: x.label()=='AN')), FILENAMEs)
			TONAMEs = list(tree.subtrees(filter=lambda x:x.label()=='TONAME'))
			TONAMEFILEs = map(lambda x: list(x.subtrees(filter=lambda x: x.label()=='AN')), TONAMEs)
		
		for i in xrange(0,len(ANs)):
			ANJSON.append(tree2json(ANs[i]))

		for i in xrange(0,len(VBs)):
			VBJSON.append(tree2json(VBs[i]))

		for i in xrange(0,len(NAMEs)):
			NJSON.append(tree2json(NAMEs[i]))

		for i in xrange(0,len(VBs)):
			verbRoot = VBJSON[i]['VERB']
			if 'VB' in verbRoot[0]:
				if verbRoot[0]['VB'][0] in ['open','close','shut','exit']:
					if isFile == True:
						actionSequence(verbRoot[0]['VB'][0],ANJSON,True)
					elif isDir == True:
						actionSequence(verbRoot[0]['VB'][0],ANJSON,False)
				elif verbRoot[0]['VB'][0] in ['make','create']:
					if isDir == True:
						createSequence(verbRoot[0]['VB'][0],NJSON,str.rstrip('\n'))				
				elif verbRoot[0]['VB'][0] in ['copy','cut','move','duplicate']:
					SOURCEs = tree2json(SOURCEs[0][0])
					DESTs = tree2json(DESTs[0][0])
					FILENAMEs = tree2json(FILENAMEs[0][0])
					cutCopy(verbRoot[0]['VB'][0],FILENAMEs,SOURCEs,DESTs)
				elif verbRoot[0]['VB'][0] in ['change','replace']:
					changeWallpaper(verbRoot[0]['VB'][0],tree2json(TONAMEFILEs[0][0]))
												
main()
