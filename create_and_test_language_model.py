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

# load test data
test_data = load_and_pad_data('europarl.test')

log_likelihood = 0
N = 0

for sent in test_data:

    toks = [el for el in sent.split(' ') if el != '']

    for i in range(len(toks) + 1 - SEQLEN):

        seq = toks[i:i + SEQLEN]
        prefix = ' '.join((seq[:-1]))
        observation = seq[-1]

        try:
            p = model[prefix][observation]

        except KeyError:
            try:
                p = model[prefix]['UNK']
            except KeyError:
                p = 1e-100  # would be improved with backoff


        log_likelihood += np.log(p)
    N += len(toks)

cross_entropy = -log_likelihood / N
perplexity = 2 ** cross_entropy
print('N:', N)
print('Perplexity:', perplexity)
