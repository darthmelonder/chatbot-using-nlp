import nltk

#check the context of the word

def checkContext(word,index,tagArr):
	if word == 'open':
		if index == len(tagArr)-1:
			#end of sentence
			#mark this as filename
			return 'AN'
		elif tagArr[i+1] not in ['NN']:
			#in between the sentence and the next word is not a determiner
			
