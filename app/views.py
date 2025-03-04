from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'app_templates/index.html')

def about(request):
    return render(request,'app_templates/about.html')

