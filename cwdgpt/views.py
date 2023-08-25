#I have created this file - Faran
from django.http import HttpResponse
from django.shortcuts import render

def index(request):

    return render(request,'index.html')
    #return HttpResponse("<h1>Home-Chat with your data using CHATGPT</h1>")
