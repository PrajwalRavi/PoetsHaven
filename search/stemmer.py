import math
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


# To convert the POS from pos_tag to one used by wordNet lemmetizer
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


dict_final = {}
dict_tf = {}
dict_idf = {}
file = 0
en_stops = set(stopwords.words('english'))
for file_no in range(0, 309):
    dict_tf[file_no] = {}
    with open("../Corpus/" + str(file_no) + ".txt", "r") as file:
        string = file.read()
        token = nltk.word_tokenize(string.lower())
        tagged = nltk.pos_tag(token)
        lemmatizer = WordNetLemmatizer()
        lemmetized_words = []  # final names to be stores in dictionary
        characters = [',',':', '.', ';', '!', '[', ']', '&', '{', '}', "''", "'", '?']
        # To lemmatize based on POS and separate the punctuation
        for word in tagged:
            if word[0] not in characters and word[0] not in en_stops:
                pos = get_wordnet_pos(word[1])
                lemmetized_words.append(lemmatizer.lemmatize(word[0], pos))

    tf_dict = {}
    for word in lemmetized_words:
        if word not in dict_tf[file_no].keys():
            dict_tf[file_no][word] = 1
        else:
            dict_tf[file_no][word] += 1
        if word not in tf_dict.keys():
            tf_dict[word] = [1, file_no]

        else:
            tf_dict[word][0] += 1

    for ele in tf_dict.keys():
        if ele not in dict_final.keys():
            dict_final[ele] = [tf_dict[ele]]
        else:
            dict_final[ele].append(tf_dict[ele])

for words in dict_final.keys():
    dict_idf[words] = math.log2(308 / (len(dict_final[words])))

for file_no in dict_tf:
    max_tf=-1
    for word in dict_tf[file_no]:
        max_tf = max(max_tf,dict_tf[file_no][word])
    for word in dict_tf[file_no]:
        dict_tf[file_no][word] = 0.4 + 0.6*(dict_tf[file_no][word]/max_tf)


for file_no in range(0, 309):
    for word in dict_tf[file_no]:
        dict_tf[file_no][word] *= dict_idf[word]

dict_tf_idf = dict_tf
outfile = open('tf-idf.dat', 'wb')
pickle.dump(dict_tf_idf, outfile)
outfile.close()
