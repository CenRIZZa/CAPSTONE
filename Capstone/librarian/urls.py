from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('librarian/', views.main, name='librarian'),
    path('librarian/recently_deleted_books/', views.recently_deleted_books, name='recently_deleted_books'),
    path('librarian/delete_book/<int:book_id>/', views.delete_book, name='delete_book'),  # Add this line
    path('librarian/delete_all_books/', views.delete_all_books, name='delete_all_books'),  # Add this line
    path('librarian/recently_deleted_books/', views.recently_deleted_books, name='delete_all_recently_deleted_books'),  # Add this line
    path('restore/<int:book_id>/', views.restore_book, name='restore_book'),
    path('delete_all_recently_deleted_books/', views.delete_all_recently_deleted_books, name='delete_all_recently_deleted_books'),
    path('toggle_availability/<int:book_id>/', views.toggle_availability, name='toggle_availability'),
    path('upload/', views.upload_view, name='upload_view'),
    path('review-request/', views.review_request, name='review_request'),
    path('borrow-requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('borrow-requests/decline/<int:request_id>/', views.decline_request, name='decline_request'),
    path('delete-approved-request/<int:request_id>/', views.delete_approved_request, name='delete_approved_request'),
    path('delete-declined-request/<int:request_id>/', views.delete_declined_request, name='delete_declined_request'),

    #path('librarian/restore_book/<int:book_id>/', views.restore_book, name='restore_book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
