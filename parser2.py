import nltk
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from nltk import CFG

text = nltk.word_tokenize("A car has a door")

tagged_text = nltk.pos_tag(text)

pos_tags = [pos for (token,pos) in nltk.pos_tag(text)]

simple_grammar = CFG.fromstring("""
  S -> NP VP
  PP -> P NP
  NP -> Det N | Det N PP
  VP -> V NP | VP PP
  Det -> 'DT'
  N -> 'NN'
  V -> 'VBZ'
  P -> 'PP'
  """)

parser = nltk.ChartParser(simple_grammar)
tree = parser.parse(pos_tags)

for tree in parser.parse(pos_tags):
	print(tree)




