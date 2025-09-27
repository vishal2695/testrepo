from django.shortcuts import render, HttpResponse

# Create your views here.

def test(request):
    return HttpResponse("Hello Vishal.")

def home(request):
    return render(request, "home.html")
