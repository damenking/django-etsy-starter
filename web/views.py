from django.shortcuts import render, redirect


def index(request):
    return redirect('home')

def home(request):
    template = 'home.html'
    return render(request, template)

def about(request):
    template = 'about.html'
    return render(request, template)

def products(request):
    template = 'products.html'
    return render(request, template)