import pickle

import nltk
from django.http import HttpResponse
from django.shortcuts import render
from nltk.corpus import stopwords, wordnet


def index(request):
    return render(request, 'search/main_page.html')


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


def get_result(message):
    words_in_query = nltk.word_tokenize(message.lower())
    en_stops = set(stopwords.words('english'))
    tagged = nltk.pos_tag(words_in_query)
    lemmatizer = nltk.WordNetLemmatizer()
    lemmetized_words = []  # final names to be stores in dictionary
    characters = [',', '.', ';', '!', '[', ']', '&', '{', '}', "''", "'", '?']
    for word in tagged:
        if word[0] not in characters and word[0] not in en_stops:
            pos = get_wordnet_pos(word[1])
            lemmetized_words.append(lemmatizer.lemmatize(word[0], pos))

    tf_idf_file = open('search/tf-idf.dat', 'rb')
    dict_tf_idf = pickle.load(tf_idf_file)
    tf_idf_file.close()

    result_dict = {}
    for file_no in dict_tf_idf:
        current_score = 0
        for word in dict_tf_idf[file_no]:
            if word in lemmetized_words:
                current_score += dict_tf_idf[file_no][word] * 1

        if current_score > 0:
            result_dict[current_score] = file_no

    result_list = sorted(result_dict.keys(), reverse=True)
    print(result_list)
    answer = []
    for result in result_list:
        answer.append(result_dict[result])
    print(answer)
    return answer


def search(request):
    message = request.GET.get('query')
    file_results = get_result(message)
    return render(request, 'search/main_page.html',
                  {'results': file_results, 'org_query': message})


def display_file(request, file_id):
    f = open("Corpus/" + file_id + ".txt", "r")
    poem_lines = f.readlines()
    s = ""
    for line in poem_lines:
        s += line + "<br>"
    return HttpResponse(s)
