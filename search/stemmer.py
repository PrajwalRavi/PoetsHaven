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
dict={}
en_stops = set(stopwords.words('english'))
for file_no in range(1,309):
	with open(str(file_no)+".txt","r") as file:
		string=file.read()
		#print (string)
		token=nltk.word_tokenize(string.lower())
		tagged=nltk.pos_tag(token)
		lemmatizer = WordNetLemmatizer()
		term=[] #final names to be stores in dictionary
		
		#To lemmatize based on POS and separate the punctuation 
		for word in tagged:
			if word[0]!="," and word[0]!="." and word[0]!=";" and word[0]!="!" and word[0] not in en_stops:
				pos=get_wordnet_pos(word[1])
				term.append(lemmatizer.lemmatize(word[0],pos))
		#print (term)
		
		for word in term:
			if word not in dict.keys():
				dict[word]=[1]
				dict[word].append(file_no)
				encoded=1
			else:
				dict[word][0]+=1
				if file_no not in dict[word]:
					dict[word].append(file_no)


filename='dictionary1'
outfile=open(filename,'wb')
pickle.dump(dict,outfile)
outfile.close()

print (dict)
