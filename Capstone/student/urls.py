from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('student',views.student, name="view"),
    path('preview/<int:book_id>/', views.prev_file, name='prev_file'),
    path('book-detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('bookmark/', views.bookmark, name='bookmark'),
    path('bookmark_toggle/', views.bookmark_toggle, name='bookmark_toggle'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('author/<str:author_name>/', views.author_detail, name='author_detail'),
    path('date/<int:publication_date>/', views.date_detail, name='date_detail'),
    path('list/<int:year>/', views.list, name='list'),
    path('author_list/', views.author_list, name='author_list'),
    path('author_detail/<str:author_name>/', views.author_detail, name='author_detail'),
    path('date/', views.date_list, name='date_list'),
    path('borrow-request/<int:book_id>/', views.borrow_request, name='borrow_request'),
    path('student/book-detail/<int:book_id>/', views.book_detail, name='book_detail'),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
