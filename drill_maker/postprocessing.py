import random
import yaml
from pathlib import Path

from botok import SylComponents, TokChunks

gis = {
    'thame': 'ས',
    'ད': 'ཀྱིས',
    'བ': 'ཀྱིས',
    'ས': 'ཀྱིས',
    'ག': 'གིས',
    'ང': 'གིས',
    'ན': 'གྱིས',
    'མ': 'གྱིས',
    'ར': 'གྱིས',
    'ལ': 'གྱིས',
}
gi = {k: v[:-1] for k, v in gis.items()}
gi['thame'] = 'འི'
la = {k: 'ར' if k == 'thame' else 'ལ' for k in gis.keys()}
tense_path = (Path(__file__).parent / 'resources' / 'tenses.yaml')
tenses = yaml.safe_load(tense_path.read_text(encoding='utf-8'))
conjugation = [
    {'me': 'པ་ཡིན', 'other': 'པ་རེད'},
    {'me': 'གི་ཡོད', 'other': 'གི་འདུག'},
    {'me': 'གི་ཡིན', 'other': 'གི་རེད'}
]

def post_process(sent):
    i = 0
    while i < len(sent):
        cur = sent[i]
        # make agreement
        if '-' in cur:
            word = sent[i-1]
            word, part = particle_agreement(word, cur)
            if part:
                sent[i-1:i+1] = [word, part]
            else:
                sent[i-1:i+1] = [word]


        # add conjugation
        if '/' in cur:
            cur = add_conjugation(cur)
            sent[i] = cur

        i += 1

    # add shad at the end
    sent = add_shad(sent)
    return sent

def add_shad(sent):
    syls = TokChunks(sent[-1]).get_syls()

    _, ending = SylComponents().get_parts(syls[-1])
    word = '་'.join(syls)
    if ending.strip('ིེོུྱྲྭ')[-1] not in 'ཀགཤ':
        word += '།'

    return sent[:-1] + [word]

def add_conjugation(verb, tense=None, person='other'):
    # do not conjugate if already has an auxiliary
    if verb.endswith('ཡིན་/') or verb.endswith('ཡོད་/') or verb.endswith('རེད་/') or verb.endswith('འདུག་/'):
        return verb[:-1]

    syls = TokChunks(verb.strip('/')).get_syls()
    if not tense:
        tense = random.choice(['past', 'present', 'future'])
        tense = {'past': 0, 'present': 1, 'future': 2}[tense]

    if syls[-1] in tenses.keys():
        syls[-1] = tenses[syls[-1]][tense]

    conj = conjugation[tense][person]
    if tense == 0:
        _, ending = SylComponents().get_parts(syls[-1])
        if not ending.strip('ིེོུྱྲྭའ'):
            conj = 'བ' + conj[1:]
    verb = '་'.join(syls + [conj]) + '་'

    return verb


def is_affixable(syl):
    stem, end = SylComponents().get_parts(syl)
    # check if syllable has suffixes
    if end and end[-1] in 'གངདནབམརལས':
        return False
    else:
        return True

def particle_agreement(word, part):
    # currently supports བྱེད་སྒྲ་ and འབྲེལ་སྒྲ་
    part = part.strip('-')
    syls = TokChunks(word).get_syls()
    ending = 'thame' if is_affixable(syls[-1]) else syls[-1][-1]
    # remove trailing འ if is thame
    if 'thame' and syls[-1][-1] == 'འ':
        syls[-1] = syls[-1][:-1]

    agreement = {'གིས་': gis, 'གི་': gi}
    for a, b in agreement.items():
        if part == a:
            if ending == 'thame':
                syls[-1] += b['thame']
            else:
                part = b[ending]

    word = '་'.join(syls) + '་'
    # ལ་དོན་ is left untouched
    if part in agreement.keys():
        part = '' if ending == 'thame' else part + '་'

    return word, part
