from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('home/', views.say_hello),
    path('join/', views.join, name='join'),
    path('search/', views.search_books, name='search_books'),
    path('login/', views.custom_login, name='login'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


