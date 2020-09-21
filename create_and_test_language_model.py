import json
import numpy as np

def load_and_pad_data(fp):
    '''
    Loads europarl sentences as strings including left and right padding.
    '''
    with open(fp, 'r', encoding='latin') as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        sentences = ['<sos> ' + t + ' <eos>' for t in lines]
    return sentences


SEQLEN = 3
train_sentences = load_and_pad_data('corpus/europarl.train')

sequences = []
for sent in train_sentences:
    toks = [el for el in sent.split(' ') if el != '']
    for i in range(len(toks)+1 - SEQLEN):
        win = toks[i:i + SEQLEN]
        sequences.append(' '.join(win))

# sort sequences
train_sequences = sorted(sequences)

# initialise variables that track progression through prefixes
# init prefix count to 1 to assume occurrence of dummy trigram
prefix_cnt = 1
prev_prefix = None

model = {}
for sequence in train_sequences:
    prefix = tuple(sequence.split(' ')[:-1])
    observation = sequence.split(' ')[-1]

    # initialise model for given prefix, assuming single occurrence of dummy trigram
    model.setdefault(prefix, {'UNK': 1})
    model[prefix].setdefault(observation, 0)

    # if iteration has moved on to another prefix, compute probabilities of trigrams with previous prefix
    if prefix != prev_prefix:
        for prev_trigram in model[prev_prefix]:
            model[prev_prefix][prev_trigram] /= prefix_cnt
        prefix_cnt = 1

    model[prefix][observation] += 1
    prefix_cnt += 1
    prev_prefix = prefix

json.dump(model, open('language_model_100percent.json', 'w'))

test_data = load_and_pad_data('corpus/test_preprocessed_europarl.en')
model = json.load(open('language_model_50percent.json'))

test_ll = 0
N = 0
for sent in test_data:
    toks = [el for el in sent.split(' ') if el != '']
    for i in range(len(toks) + 1 - SEQLEN):
        ll = 0
        seq = toks[i:i + SEQLEN]
        condition = ' '.join(seq[:-1])
        observation = seq[-1]
        try:
            ll += np.log(model[condition][observation])
        except KeyError:
            ll += np.log(1e-100)
        test_ll += ll
        N += 1

cross_entropy = -1 * test_ll / N
pp1 = 2**cross_entropy
