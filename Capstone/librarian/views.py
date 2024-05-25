from datetime import datetime
import os
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import BookForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import ApprovedRequest, Books, Category, LANGUAGE_CHOICES, BorrowRequest, DeclinedRequest
from .models import SubCategory
from django.db.models.functions import TruncYear



@login_required
def main(request):
    books = Books.objects.filter(deleted_at__isnull=True)
    recently_deleted_books = Books.objects.filter(deleted_at__isnull=False)
    borrow_requests = BorrowRequest.objects.filter(expires_at__gt=timezone.now())
    approved_requests = ApprovedRequest.objects.all()
    declined_requests = DeclinedRequest.objects.all()
    language_choices = LANGUAGE_CHOICES

    # Generate a list of years from the book dates
    years = Books.objects.annotate(year=TruncYear('Date')).values_list('year', flat=True).distinct().order_by('-year')

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if book_id:
            book = Books.objects.get(pk=book_id)
            book.deleted_at = timezone.now()
            book.save()
            return redirect('librarian')

    # Filtering
    year_filter = request.GET.get('year')
    language_filter = request.GET.get('language')
    file_type_filter = request.GET.get('file_type')
    category_filter = request.GET.get('category')

    if year_filter:
        try:
            year = int(year_filter)
            books = books.filter(Date__year=year)
        except ValueError:
            pass  # Handle invalid year input gracefully

    if language_filter:
        books = books.filter(Language=language_filter)
    if file_type_filter:
        if file_type_filter == 'eBook':
            books = books.filter(eBook=True)
        elif file_type_filter == 'Research Paper':
            books = books.filter(research_paper=True)
    if category_filter:
        books = books.filter(Category__name=category_filter)

    subcategories = SubCategory.objects.all()
    categories = Category.objects.all()

    context = {
        'books': books,
        'recently_deleted_books': recently_deleted_books,
        'language_choices': language_choices,
        'categories': categories,
        'subcategories': subcategories,
        'borrow_requests': borrow_requests,
        'approved_requests': approved_requests,
        'declined_requests': declined_requests,
        'years': [date.year for date in years],  # Extract the year from each date
    }

    return render(request, 'main.html', context)

@login_required
def upload_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('librarian')
    else:
        form = BookForm()
    subcategories = SubCategory.objects.all()
    categories = Category.objects.all()
    
    return render(request, 'main.html', {'form': form, 'categories': categories, 'subcategories':subcategories,})


@login_required
def approve_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    ApprovedRequest.objects.create(
        book=borrow_request.book,
        requested_by=borrow_request.requested_by,
        requested_at=borrow_request.requested_at,
        #file_type=borrow_request.book.get_file_type()
    )
    borrow_request.delete()
    return redirect('librarian')


@login_required
def decline_request(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    DeclinedRequest.objects.create(
        book=borrow_request.book,
        requested_by=borrow_request.requested_by,
        requested_at=borrow_request.requested_at,
        #file_type=borrow_request.book.get_file_type()
    )
    borrow_request.delete()
    return redirect('librarian')

@login_required
def delete_approved_request(request, request_id):
    approved_request = get_object_or_404(ApprovedRequest, id=request_id)
    approved_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('librarian')))

@login_required
def delete_declined_request(request, request_id):
    declined_request = get_object_or_404(DeclinedRequest, id=request_id)
    
    if request.method == 'POST':
        declined_request.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('librarian')))
    else:
        pass

def delete_expired_requests():
    expired_requests = BorrowRequest.objects.filter(expires_at__lt=timezone.now())
    expired_requests.delete()



@login_required
def delete_book(request, book_id):
    book = Books.objects.get(pk=book_id)
    book.deleted_at = timezone.now()
    book.save()
    return redirect('librarian')

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
    book.deleted_at = None
    book.save()
    return redirect('librarian')

@login_required
def delete_all_recently_deleted_books(request):
    if request.method == 'POST':
        recently_deleted_books = Books.objects.filter(deleted_at__isnull=False)
        for book in recently_deleted_books:
            if book.BookFile:
                book.BookFile.delete(save=False)
            if book.BookImage:
                book.BookImage.delete(save=False)
        recently_deleted_books.delete()
    return redirect('librarian')

def delete_recently_deleted_books(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Books, id=book_id)
        if book.BookFile:
            book.BookFile.delete(save=False)
        if book.BookImage:
            book.BookImage.delete(save=False)
        book.delete()
    return redirect('librarian')

@login_required
def toggle_availability(request, book_id):
    book = Books.objects.get(id=book_id)
    book.available = not book.available
    book.save()
    return redirect('librarian')

def logout_user(request):
    logout(request)
    messages.success(request, "You were Logged Out!")
    return redirect('login_user')

@login_required
def approve_request_view(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    if request.method == 'POST':
        ApprovedRequest.objects.create(
            book=borrow_request.book,
            requested_by=borrow_request.requested_by,
            requested_at=borrow_request.requested_at,
        )
        borrow_request.delete()
        borrow_request.book.borrowed.add(request.user)
        return redirect('librarian')
    return redirect('librarian')

@login_required
def decline_request_view(request, request_id):
    borrow_request = get_object_or_404(BorrowRequest, id=request_id)
    if request.method == 'POST':
        DeclinedRequest.objects.create(
            book=borrow_request.book,
            requested_by=borrow_request.requested_by,
            requested_at=borrow_request.requested_at,
        )
        borrow_request.delete()
        return redirect('librarian')
    return redirect('librarian')



def go_back(request):
    return redirect('main') 

