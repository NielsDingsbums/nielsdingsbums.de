from django.shortcuts import render
from .models import Posts

# Create your views here.
def index(request):
	#return HttpResponse('<h1>HELLO FROM POSTS</h1>')

	posts = Posts.objects.all()[::-1]

	context = {
		'title': 'Latest Posts',
		'posts': posts
	}

	return render(request, 'posts/index.html', context)

def details(request, id):
	post = Posts.objects.get(id=id)

	context = {
		'post': post
	}

	return render(request, 'posts/details.html', context)

