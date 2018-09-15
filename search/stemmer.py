import math

from nltk.corpus import stopwords
import nltk
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#To convert the POS from pos_tag to one used by wordNet lemmetizer
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
dict_final={}
#tf_dict={}
file=0
en_stops = set(stopwords.words('english'))
for file_no in range(1,309):
	with open("../Corpus/"+str(file_no)+".txt","r") as file:
		string=file.read()
		#print (string)
		token=nltk.word_tokenize(string.lower())
		tagged=nltk.pos_tag(token)
		lemmatizer = WordNetLemmatizer()
		term=[] #final names to be stores in dictionary
		characters=[',','.',';','!','[',']','&','{','}', "''","'"]
		#To lemmatize based on POS and separate the punctuation 
		for word in tagged:
			if word[0] not in characters and word[0] not in en_stops:
				pos=get_wordnet_pos(word[1])
				term.append(lemmatizer.lemmatize(word[0],pos))
		#print (term)
		
	"""	for word in term:
			if word not in dict.keys():
				dict[word]=[1]
				dict[word].append(file_no)

			else:
				dict[word][0]+=1
				if file_no not in dict[word]:
					dict[word].append(file_no)"""
	tf_dict={}
	for word in term:
		if word not in tf_dict.keys():
			tf_dict[word]=[1,file_no]

		else:
			tf_dict[word][0]+=1

	for ele in tf_dict.keys():
		if ele not in dict_final.keys():
			dict_final[ele]=[tf_dict[ele]]
		else:
			dict_final[ele].append(tf_dict[ele])


# filename='freq_doc'
# outfile=open(filename,'wb')
# pickle.dump(dict_final,outfile)
# outfile.close()

"""mydict=sorted(dict.keys())

filename='terms'
outfile=open(filename,'wb')
pickle.dump(mydict,outfile)
outfile.close()"""
df_dict={}
for words in dict_final.keys():
	df_dict[words]=math.log2(308/(len(dict_final[words])))
print (df_dict)