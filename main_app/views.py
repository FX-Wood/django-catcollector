from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Cat, CatToy
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cats_show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/show.html', {'cat': cat})


class CatCreate(CreateView):
    model = Cat
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect('/cats')

class CatUpdate(UpdateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age', 'cattoys']
    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # print(form.cattoys)
        # we are gonna add some stuff here
        form.save()
        return HttpResponseRedirect(f"/cats/{str(self.object.pk)}")

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats'

def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

class CatToyCreate(CreateView):
    model = CatToy
    fields = '__all__'
    success_url = '/cattoys'

class CatToyUpdate(UpdateView):
    model = CatToy
    fields = ['name', 'color']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # we are gonna add some stuff here
        self.object.save()
        return HttpResponseRedirect(f"/cats/{str(self.object.pk)}")

class CatToyDelete(DeleteView):
    model = CatToy
    success_url = '/cattoys'

def cattoys_index(request):
    cattoys = CatToy.objects.all()
    return render(request, 'cattoys/index.html', {'cattoys': cattoys})

def cattoys_show(request, cattoy_id):
    cattoy = CatToy.objects.get(id=cattoy_id)
    return render(request, 'cattoys/show.html', {'toy': cattoy})

def login_view(request):
    if request.method == 'POST':
        # Authenticate the user
        # parse post body with form
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            # if authentication fails, user will be None
            if not user:
                # django allows for deactivating users, 
                # which leaves their record intact but disables login
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print('The account has been disabled')
            
                print('username or password are incorrect')
    
    # if method is not POST
    else:
        # send user the form
        form = LoginForm()
        return render(request, 'login.html', {'form', form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(f"/user/{user.username}/")
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form', form})
