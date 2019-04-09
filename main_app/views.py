from django.shortcuts import render
from django.http import HttpResponse

class Cat():
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

cats = [
    Cat('Lolo', 'tabby', 'foul little demon', 3),
    Cat('Sachi', 'tortoise shell', 'small and feisty', 0),
    Cat('Maki', 'flamepoint siamese', 'white and ornery', 10),
]

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    return render(request, 'cats/index.html', {'cats': cats})