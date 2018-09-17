import math
import pickle

import nltk
from django.http import HttpResponse
from django.shortcuts import render
from nltk.corpus import stopwords, wordnet

from search.models import Poem


def index(request):
    return render(request, 'search/main_page.html')


# Function to convert POS into Wordnet Convention
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


# Processing the query and returning the search results
def get_result(message):
    words_in_query = nltk.word_tokenize(message.lower())  # Tokenisation
    en_stops = set(stopwords.words('english'))  # Stopwords acquirement
    tagged = nltk.pos_tag(words_in_query)  # Tagging for POS
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_words = []  # final names to be stores in dictionary
    characters = [',', '.', ';', '!', '[', ']', '&', '{', '}', "''", "'", '?']
    for word in tagged:
        if word[0] not in characters and word[0] not in en_stops:
            pos = get_wordnet_pos(word[1])  # POS conversion to map with WordNet Lemmatizer
            lemmatized_words.append(lemmatizer.lemmatize(word[0], pos))

    tf_idf_file = open('search/tf-idf.dat', 'rb')  # Unpickling the stored tf-idf file for query matching and ranking
    dict_tf_idf = pickle.load(tf_idf_file)
    tf_idf_file.close()

    result_dict = {}
    # Assigning tf-idf score for each word in query with each file
    for file_no in dict_tf_idf:
        current_score = 0
        for word in dict_tf_idf[file_no]:
            if word in lemmatized_words:
                current_score += dict_tf_idf[file_no][word] * 1  # dot product

        current_score /= math.sqrt(len(lemmatized_words))  # divide by sqrt(length of query)
        if current_score > 0:
            result_dict[current_score] = file_no

    result_list = sorted(result_dict.keys(), reverse=True)
    answer = []
    print(result_list)
    for result in result_list:
        answer.append(result_dict[result])
    return answer


def search(request):
    """
        Handles the queries given by the user.
        Calls the get_result() function which calculates and returns the appropriate
        search results.
    """
    message = request.GET.get('query')
    file_results = get_result(message)
    file_objects = []  # stores the file object associated with each file number in file_results
    poem_names = []
    for file_num in file_results:
        obj = Poem.objects.get(id=file_num)
        if obj.title not in poem_names:
            file_objects.append(obj)
            poem_names.append(obj.title)

    if len(file_objects) > 10:
        file_objects = file_objects[:10]
    return render(request, 'search/main_page.html',
                  {'results': file_objects, 'org_query': message})


def display_file(request, file_id):
    """
        Renders the appropriate file to be displayed based on file_id argument.
    """
    f = open("Corpus/" + file_id + ".txt", "r")
    poem_lines = f.readlines()
    s = ""
    for line in poem_lines:
        s += line + "<br>"
    return HttpResponse(s)


def refresh(request):
    """
        Updates the database with file_id, poet, poem name from the corpus
    """
    print("Refresh initiated")
    for i in range(0, 309):
        f = open('Corpus/' + str(i) + '.txt', 'r')
        lines = f.readlines()
        title2 = lines[0]
        poet2 = lines[1]
        poem_obj = Poem(id=i, title=title2, poet=poet2)
        poem_obj.save()
        print(i)
        f.close()
    return None
