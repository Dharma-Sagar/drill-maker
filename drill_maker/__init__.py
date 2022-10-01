from pathlib import Path

from .cfg import CFG
from .parse_cfg_terminals import parse_cfg_terminals
from .postprocessing import post_process

def gen_sents(grammar=None, symbol='S', num=20):
    if not grammar:
        grammar = ''
        for f in (Path(__file__).parent / 'patterns').glob('*patterns.txt'):
            grammar += f.read_text(encoding='utf-8') + '\n'

    grmr = CFG(f'{grammar}\n{parse_cfg_terminals()}')

    generated = []
    for _ in range(num):
        gen = grmr.gen_random_convergent(symbol)
        gen = post_process(gen)
        generated.append(gen)

    return generated
