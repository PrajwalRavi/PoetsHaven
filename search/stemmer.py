import math

from nltk.corpus import stopwords
import nltk
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


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
dict_tf={}
# tf_dict={}
file = 0
en_stops = set(stopwords.words('english'))
for file_no in range(1, 309):
    dict_tf[file_no]={}
    with open("../Corpus/" + str(file_no) + ".txt", "r") as file:
        string = file.read()
        # print (string)
        token = nltk.word_tokenize(string.lower())
        tagged = nltk.pos_tag(token)
        lemmatizer = WordNetLemmatizer()
        lemmetized_words = []  # final names to be stores in dictionary
        characters = [',', '.', ';', '!', '[', ']', '&', '{', '}', "''", "'",'?']
        # To lemmatize based on POS and separate the punctuation
        for word in tagged:
            if word[0] not in characters and word[0] not in en_stops:
                pos = get_wordnet_pos(word[1])
                lemmetized_words.append(lemmatizer.lemmatize(word[0], pos))

    tf_dict = {}
    for word in lemmetized_words:
        if word not in dict_tf[file_no].keys():
            dict_tf[file_no][word]=1
        else:
            dict_tf[file_no][word]+=1
        if word not in tf_dict.keys():
            tf_dict[word] = [1, file_no]

        else:
            tf_dict[word][0] += 1

    for ele in tf_dict.keys():
        if ele not in dict_final.keys():
            dict_final[ele] = [tf_dict[ele]]
        else:
            dict_final[ele].append(tf_dict[ele])

df_dict = {}
for words in dict_final.keys():
    df_dict[words] = math.log2(308 / (len(dict_final[words])))
# print(df_dict)
print(dict_tf)
"""mydict=sorted(dict.keys())

filename='terms'
outfile=open(filename,'wb')
pickle.dump(mydict,outfile)
outfile.close()"""