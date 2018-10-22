from django.urls import path
from . import views

urlpatterns = [
	path ('', views.index),
	path ('details/<int:id>/', views.details, name='details'),
	path ('migrate/', views.migrate),
	path('add/', views.add),
	path('edit/<int:id>/', views.edit),
	path('del/<int:id>/', views.delete),
	path('deletion_complete/<int:id>', views.deletion_copmplete),
	path('author/<str:name>/', views.author)
]
