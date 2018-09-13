from django.shortcuts import render


def index(request):
    return render(request, 'search/main_page.html')


def search(request):
    message = request.GET.get('query')
    results = ['Pro','Boy','Girl']
    return render(request, 'search/main_page.html', {'results':results,'org_query':message})