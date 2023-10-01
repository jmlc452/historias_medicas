from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'username or password is incorrect',
        })
    else:
        login(request, user)
        return redirect('inicio')
