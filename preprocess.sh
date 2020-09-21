'''
Run process.sh to clean the Europarl-v7.nl-en.en corpus, create a lexicon, and split data in train/test (80/20)
'''


# cleans dorpus and creates lexicon

cat europarl-v7.nl-en.en | tr '[:upper:]' '[:lower:]' | tr '´' "'" | tr -d '[:punct:]' > europarl.clean
sed -i '/^ *$/d' < europarl.clean
cat europarl.clean | tr ' ' '\n' | sort -u > europarl.lexicon

# adds missing pronunciations
pip install g2p_en
python complete_lexicon.py

# when previous steps are followed exactly, corpus and train and test sizes (80%/20%) are as follows:

# wc -l corpus/preprocessed_europarl.en
# 1981134
# bc <<<"1981134*0.20"
# 396226.80
# bc <<<"1981134-396226"
# 1584908

# split data
tail -n 396226 < europarl.clean > europarl.test
head -n 1584908 < europarl.clean > europarl.train

