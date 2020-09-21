from g2p_en import G2p

with open('cmudict.dict', 'r') as f:
    lines = f.readlines()

cmudict = {}
for l in lines:
    l = l.strip().split(' ')
    graphemes = l[0]
    phonemes = l[1:]
    cmudict[graphemes] = phonemes

with open('europarl.lexicon', 'r') as f:
    europarl_lexicon = [el.strip() for el in f.readlines()]

g2p = G2p()

complete_dict = []
for el in europarl_lexicon:
    if el in cmudict:
        output = [el] + cmudict[el]
    else:
        output = [el] + g2p(el)
    complete_dict.append(' '.join(output))

with open('europarl.lexicon', 'w') as f:
    for el in complete_dict:
        f.write(el + '\n')