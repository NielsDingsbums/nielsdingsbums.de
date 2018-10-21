from django.shortcuts import render, redirect
from posts.models import Posts

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def index(request):
	posts = Posts.objects.all()[:6][::-1]


	for post in posts:
		previewItems = post.body.split()[:35]
		preview = ' '.join(previewItems)

		post.preview = preview

	context = {
		'posts': posts
	}

	return render (request, 'home/index.html', context)
