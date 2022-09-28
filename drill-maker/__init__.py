from pathlib import Path

from nltk.parse.generate import generate, demo_grammar
from nltk import CFG


grammar = CFG.fromstring((Path().cwd() / 'grammars' / 'A0.txt').read_text(encoding='utf-8'))

print(grammar)

