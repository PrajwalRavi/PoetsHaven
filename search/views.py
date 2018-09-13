from django.shortcuts import render


def index(request):
    return render(request, 'search/main_page.html')

def get_result(message):


def search(request):
    message = request.GET.get('query')
    results = get_result(message)
    return render(request, 'search/main_page.html', {'results':results,'org_query':message})