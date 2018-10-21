from . import views

urlpatterns = [
    path('', views.index, name='account'),
    path('change_password', views.change_password, name='change_password')
]
