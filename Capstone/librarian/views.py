from datetime import datetime
import os
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
#from .forms import RestoreBookForm
from .forms import BookForm
from .models import ApprovedRequest, Books, Category, LANGUAGE_CHOICES, BorrowRequest, DeclinedRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib import messages


@login_required
def upload_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('librarian')
    else:
        form = BookForm()

    categories = Category.objects.all()
    return render(request, 'main.html', {'form': form, 'categories': categories})


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import BorrowRequest, ApprovedRequest, DeclinedRequest

def review_request(request):
    borrow_requests = BorrowRequest.objects.filter(expires_at__gt=timezone.now())
    approved_requests = ApprovedRequest.objects.all()
    declined_requests = DeclinedRequest.objects.all()
    context = {
        'borrow_requests': borrow_requests,
        'approved_requests': approved_requests,
        'declined_requests': declined_requests,
    }
    return render(request, 'review_request.html', context)

def approve_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    ApprovedRequest.objects.create(
        book=borrow_request.book,
        requested_by=borrow_request.requested_by,
        requested_at=borrow_request.requested_at,
    )

    borrow_request.delete()

    return redirect('review_request')

def decline_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)

    DeclinedRequest.objects.create(
        book=borrow_request.book,
        requested_by=borrow_request.requested_by,
        requested_at=borrow_request.requested_at,
    )

    borrow_request.delete()

    return redirect('review_request')

@login_required
def delete_approved_request(request, request_id):
    approved_request = get_object_or_404(ApprovedRequest, id=request_id)
    approved_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('review_request')))

@login_required
def delete_declined_request(request, request_id):
    declined_request = get_object_or_404(DeclinedRequest, id=request_id)
    declined_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('review_request')))

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


def logout_user(request):
    logout(request)
    messages.success(request, "You were Logged Out!")
    url = reverse('login_user')
    return redirect(url)

@login_required
def borrow_requests_view(request):
    borrow_requests = BorrowRequest.objects.all()
    return render(request, 'borrow_requests.html', {'borrow_requests': borrow_requests})

@login_required
def approve_request_view(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    if request.method == 'POST':
        ApprovedRequest.objects.create(
            book=borrow_request.book,
            requested_by=borrow_request.requested_by,
            requested_at=borrow_request.requested_at
        )
        borrow_request.delete()
        return redirect('borrow_requests')
    return redirect('borrow_requests')

@login_required
def decline_request_view(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    if request.method == 'POST':
        DeclinedRequest.objects.create(
            book=borrow_request.book,
            requested_by=borrow_request.requested_by,
            requested_at=borrow_request.requested_at
        )
        borrow_request.delete()
        return redirect('borrow_requests')
    return redirect('borrow_requests')




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