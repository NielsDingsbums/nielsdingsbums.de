from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'account/index.html')


def signup(request):
	context = {}

	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('/')

	else:
		form = SignUpForm()


	context["form"] = form
	return render(request, 'registration/signup.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('account/')

    else:
        form = PasswordChangeForm(request)

    return render(request, 'account/change_password.html', {'form': form})
