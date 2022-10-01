from drill_maker import gen_sents

g = "S -> LOC1 OBJ3 'ཡོད་'"

sents = gen_sents(g)
for s in sents:
    print(' '.join(s))