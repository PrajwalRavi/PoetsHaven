import math
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


def get_wordnet_pos(treebank_tag):
    """
    Function to convert the POS(Parts of Speech) from pos_tag to one used by wordNet lemmetizer
    """
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

for file_no in range(0, 309):  # Run through each file to collect the words
    dict_tf[file_no] = {}

    with open("../Corpus/" + str(file_no) + ".txt", "r") as file:
        string = file.read()
        token = nltk.word_tokenize(string.lower())  # tokenisation
        tagged = nltk.pos_tag(token)  # tagging for POS
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []  # final names to be stores in dictionary
        characters = [',', ':', '.', ';', '!', '[', ']', '&', '{', '}', "''", "'", '?']

        # To lemmatize based on POS and separate the punctuation
        for word in tagged:
            if word[0] not in characters and word[0] not in en_stops:
                pos = get_wordnet_pos(
                    word[1])  # To convert the POS from pos_tag to one recognised by wordNet lemmetizer
                lemmatized_words.append(lemmatizer.lemmatize(word[0], pos))

    # To create a term frequency dictionary for each file in corpus
    tf_dict = {}
    for word in lemmatized_words:
        if word not in dict_tf[file_no].keys():
            dict_tf[file_no][word] = 1
        else:
            dict_tf[file_no][word] += 1
        if word not in tf_dict.keys():
            tf_dict[word] = [1, file_no]

        else:
            tf_dict[word][0] += 1

    # To add this dictionary to a final dictionary
    for ele in tf_dict.keys():
        if ele not in dict_final.keys():
            dict_final[ele] = [tf_dict[ele]]
        else:
            dict_final[ele].append(tf_dict[ele])

# To create the idf model dictionary
for words in dict_final.keys():
    dict_idf[words] = math.log2(308 / (len(dict_final[words])))

# To create a file containing the idf model data structure. Process is called pickling
file_open = open('words.dat', 'wb')
pickle.dump(list(dict_idf.keys()), file_open)
file_open.close()

# To create the tf-idf for each word in each file
for file_no in dict_tf:
    max_tf = -1
    for word in dict_tf[file_no]:
        max_tf = max(max_tf, dict_tf[file_no][word])
    for word in dict_tf[file_no]:
        dict_tf[file_no][word] = 0.4 + 0.6 * (dict_tf[file_no][word] / max_tf)

# To normalise the cosine multiplication
for file_no in range(0, 309):
    sum = 0
    for word in dict_tf[file_no]:
        dict_tf[file_no][word] *= dict_idf[word]
        sum += math.pow(dict_tf[file_no][word], 2)
    for word in dict_tf[file_no]:
        dict_tf[file_no][word] /= math.sqrt(sum)

# To create a file containing the tf-idf model data structure
dict_tf_idf = dict_tf
outfile = open('tf-idf.dat', 'wb')
pickle.dump(dict_tf_idf, outfile)
outfile.close()
