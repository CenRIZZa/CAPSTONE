from datetime import datetime
import os
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
#from .forms import RestoreBookForm
from .forms import BookForm
from .models import Books, Category, LANGUAGE_CHOICES, BorrowRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



@login_required
def upload_view(request):
    form = BookForm()
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('librarian')  # Redirect to a page showing the list of products
    
    # Retrieve all categories from the database
    categories = Category.objects.all()
    
    return render(request, 'main.html', {'form': form, 'categories': categories})


def review_request(request):
    borrow_requests = BorrowRequest.objects.filter(expires_at__gt=timezone.now())
    context = {'borrow_requests': borrow_requests}
    return render(request, 'review_request.html', context)

def approve_request(request, request_id):
    # Get the BorrowRequest object
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    # Update the Books model to mark the book as borrowed
    book = borrow_request.book
    book.borrowed.add(borrow_request.requested_by)
    book.save()

    # Delete the BorrowRequest object
    borrow_request.delete()

    return redirect('review_request')

def decline_request(request, request_id):
    borrow_request = BorrowRequest.objects.get(pk=request_id)
    # Logic for declining the request (e.g., delete the request)
    borrow_request.delete()
    return redirect('review_request')

def delete_expired_requests():
    expired_requests = BorrowRequest.objects.filter(expires_at__lt=timezone.now())
    expired_requests.delete()
    
@login_required
def main(request):
    books = Books.objects.filter(deleted_at__isnull=True)
    recently_deleted_books = Books.objects.filter(deleted_at__isnull=False)
    language_choices = LANGUAGE_CHOICES  # Add this line to get the language choices

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if book_id:
            book = Books.objects.get(pk=book_id)
            book.deleted_at = timezone.now()
            book.save()
            return redirect('main')
        
    categories = Category.objects.all()
    return render(request, 'main.html', {'books': books, 'recently_deleted_books': recently_deleted_books, 'language_choices': language_choices, 'categories': categories})


@login_required
def delete_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.deleted_at = timezone.now()  # Mark the book as deleted
    book.save()
    return redirect('librarian')

@login_required
def recently_deleted_books(request):
    recently_deleted_books = Books.objects.filter(deleted_at__isnull=False)
    categories = Category.objects.all()
    return render(request, 'recently_deleted_books.html', {'recently_deleted_books': recently_deleted_books, 'categories': categories})


#marjks the book deleted
@login_required
def delete_all_books(request):
    books = Books.objects.filter(deleted_at__isnull=True)
    for book in books:
        book.deleted_at = timezone.now()
        book.save()
    return redirect('librarian')

@login_required
def restore_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.deleted_at = None  # Mark the book as not deleted
    book.save()
    return redirect('recently_deleted_books')

@login_required
def delete_all_recently_deleted_books(request):
    if request.method == 'POST':
        # Get all recently deleted books
        recently_deleted_books = Books.objects.filter(deleted_at__isnull=False)

        # Delete files from the server
        for book in recently_deleted_books:
            # Delete the book file
            if book.BookFile:
                book.BookFile.delete(save=False)

            # Delete the book image
            if book.BookImage:
                book.BookImage.delete(save=False)

        # Permanently delete all recently deleted books
        recently_deleted_books.delete()

    return redirect('recently_deleted_books')

@login_required
def toggle_availability(request, book_id):
    book = Books.objects.get(id=book_id)
    book.available = not book.available  # Toggle the availability status
    book.save()
    return redirect('librarian')  # Redirect back to the books page
'''
def restore_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.deleted_at = None
    book.save()
    return redirect('librarian')
'''

'''
#taga display sa recnelty deleted
def recently_deleted_books(request):
    recently_deleted = RecentlyDeletedBooks.objects.all()
    return render(request, 'recently_deleted_books.html', {'recently_deleted': recently_deleted})


#pang librarian
def delete_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.move_to_recently_deleted()
    book.save()
    return redirect('librarian')

def delete_all_books(request):
    if request.method == 'POST':
        # Process form submission
        for book in Books.objects.all():
            book.move_to_recently_deleted()
        return redirect('librarian')  # Redirect to the home page after deletion
    return render(request, 'main.html')  # Render the main.html template

def restore_book(request, book_id):
    if request.method == 'POST':
        # Restore the book
        book = RecentlyDeletedBooks.objects.get(pk=book_id)
        book.restore()
        book.save()
    return redirect('recently_deleted_books')


def delete_all_recently_deleted_books(request):
    if request.method == 'POST':
        # Process form submission
        for book in RecentlyDeletedBooks.objects.all():
            # Delete associated files
            if book.BookImage:
                image_path = book.BookImage.path
                if os.path.isfile(image_path):
                    new_image_path = os.path.join(settings.MEDIA_ROOT, 'deleted_books', 'images', os.path.basename(image_path))
                    try:
                        os.rename(image_path, new_image_path)
                    except FileExistsError:
                        # File already exists in destination, do nothing
                        pass
            if book.BookFile:
                file_path = book.BookFile.path
                if os.path.isfile(file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'deleted_books', 'files', os.path.basename(file_path))
                    try:
                        os.rename(file_path, new_file_path)
                    except FileExistsError:
                        # File already exists in destination, do nothing
                        pass
            book.delete()
        return redirect('recently_deleted_books')  # Redirect to the recently_deleted_books page after deletion
    return render(request, 'recently_deleted_books.html')
'''