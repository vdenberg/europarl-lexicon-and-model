### Creates lexicon and 3-gram language model.
Steps:

0) Get English section of the Dutch-English parallel Europarl corpus from http://statmt.org/europarl/.

Then run _preprocess.sh_ to:

1) Preprocess the corpus so that it ignores capitalization and punctuation.
2) Compare the lexicon from the cleaned corpus from step 1 with the provided lexicon and add out-of-vocabulary tokens to the lexicon.
3) Generate pronunciations for the OOV words with g2p toolkit.
4) Split the corpus into test & training sets (20/80).

Then run _create_and_test_language_model.py_ to:

5) Build a 3-gram Language Model using the training set.
6) Using the test set, calculate the perplexity of the created Language Model.


