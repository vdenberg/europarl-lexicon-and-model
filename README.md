Get English section of the Dutch-English parallel Europarl corpus from here: http://statmt.org/europarl/

Then run preprocess.sh to:

1) Preprocess the text (corpus) so that it ignores capitalization and punctuation
2) Compare the lexicon from the cleaned corpus from step 1 with the provided lexicon and add OOV’s (out of vocabulary words) to the lexicon
3) Generate pronunciations for the OOV words that you have found. You could use a grapheme-to-phoneme toolkit or e.g. espeak, or you could try to find pronunciations from some other source.
(uses complete_lexicon.py).
4) Split the corpus into test & training sets (20% : 80%).

Then run create_and_test_language_model.py to:

5) Build a 3-gram Language Model using the training set.
6) Using the test set, calculate the perplexity of the created Language Model (you can use SRILM toolkit or whatever you prefer).


