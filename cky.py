#Implementation of CKY algorithm

def CKY(t):
	#A CFG
	grammar =        """S -> NP VP 
			  S -> VP 
			  NP -> MODAL PRON | DET NP | NOUN VF | NOUN | DET NOUN | DET FILENAME
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
			  DET -> 'AT'"""

	grammar_list = grammar.split('\n')

	new_grammar = []

	for item in grammar_list:
		item = item.strip()
		new_grammar.append(item)

	#now save in a chart or a dictionary

	rules = {}

	for item in new_grammar:
		arr = item.split('->')
		lhs = arr[0].strip()
		rhs = arr[1].strip()
		if '|' in rhs:
			rhs_chunks = rhs.split('|')
			for rc in rhs_chunks:
				rc = rc.strip()
				rc = rc.strip("'")
				rules[rc] = lhs
		else:
			rhs = rhs.strip("'")		
			rules[rhs] = lhs


	table = {}

	sentence = t

	#sentence = ['']+sentence

	n = len(sentence)

	table[(0,1)] = sentence[1]

	for j in range(1,n):
		table[(j-1,j)] = rules[sentence[j]]
		for i in xrange(j-2,-1,-1):
			for k in xrange(i+1,j):
				if (i,k) in table and (k,j) in table:
					if table[(i,k)]+' '+table[(k,j)] in rules:
						if (i,j) in table:
							table[(i,j)] = table[(i,j)]+rules[table[(i,k)]+" "+table[(k,j)]]
						else:
							table[(i,j)] = rules[table[(i,k)]+" "+table[(k,j)]]

	print(table)
	if 'S' in table[(0,n-1)]:
		print("Parsed")

