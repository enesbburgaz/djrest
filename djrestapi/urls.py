
from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('admin', admin.site.urls),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('book', views.book, name='book'),
]
