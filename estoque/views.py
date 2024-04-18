from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def estoque(request):
    return render(request, 'estoque.html')

def produto(request):
    return render(request, 'produto.html')