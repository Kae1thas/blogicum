from django.shortcuts import render

def index(request):
    context = {"posts": posts}
    return render(request, "blog/index.html", context)

def about(request):
    return render(request, 'pages/about.html')

def rules(request):
    return render(request, 'pages/rules.html')
