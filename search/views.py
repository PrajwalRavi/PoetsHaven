from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'search/main_page.html')

def get_result(message):
    pass

def search(request):
    message = request.GET.get('query')
    results = ['1','2','3','200']
    return render(request, 'search/main_page.html', {'results':results,'org_query':message})


def display_file(request, file_id):
    f= open("Corpus/"+file_id+".txt","r")
    poem_lines = f.readlines()
    s=""
    for line in poem_lines:
        s+=line+"<br>"
    return HttpResponse(s)