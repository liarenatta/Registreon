from django.shortcuts import render

def inicio(request):
    return render(request, 'inicio.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def login(request):
    return render(request, 'login.html')

def anonimo(request):
    return render(request, 'anonimo.html')

def ocorrencias(request):
    return render(request, 'ocorrencias.html')

def funcionario_login(request):
    return render(request, 'funcionario_login.html')


