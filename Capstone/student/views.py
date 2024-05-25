from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from librarian.models import Books, BorrowRequest, ApprovedRequest, DeclinedRequest
from django.urls import reverse
from django.db.models import Count, F
import logging

def student(request):
    all_books = Books.objects.all()
    top_viewed_books = Books.objects.all().order_by('-PageViews')[:7]

    books_per_category = {}
    for book in all_books:
        for category in book.Category.all():
            if category not in books_per_category:
                books_per_category[category] = []
            books_per_category[category].append(book)

    # Fetch all unique authors
    authors = Books.objects.values_list('Author', flat=True).distinct()

    # Fetch distinct years
    years = Books.objects.values_list('Date__year', flat=True).distinct()

    # Fetch research papers
    research_papers = Books.objects.filter(research_paper=True)

    # Fetch eBooks
    ebooks = Books.objects.filter(eBook=True)

    return render(request, 'student_content.html', {
        'books_per_category': books_per_category,
        'authors': authors,
        'years': years,
        'top_viewed_books': top_viewed_books,
        'research_papers': research_papers,  # Include research papers in the context
        'ebooks': ebooks,  # Include eBooks in the context
    })
    
def author_list(request):
    authors = Books.objects.values_list('Author', flat=True).distinct()
    return render(request, 'author_list.html', {'authors': authors})

def author_detail(request, author_name):
    # Filter books by the author's name
    author_books = Books.objects.filter(Author=author_name)
    return render(request, 'author_content.html', {'author_books': author_books, 'author_name': author_name})

def date_list(request):
    years = Books.objects.dates('Date', 'year').order_by('-Date')
    return render(request, 'date_detail.html', {'years': years})

def date_detail(request, publication_date):
    # Filter books by the publication date
    date_books = Books.objects.filter(Date__year=publication_date)
    return render(request, 'book_year_content.html', {'year_books': date_books, 'year': publication_date})

def list(request):
    years = Books.objects.dates('Date', 'year').order_by('-Date')
    return render(request, 'book_year_content.html', {'years': years})

def author_detail(request, author_name):
    # Filter books by the author's name
    author_books = Books.objects.filter(Author=author_name)
    return render(request, 'author_content.html', {'author_books': author_books, 'author': author_name})

def book_info(request, book_id):
    book = Books.objects.get(pk=book_id)
    return render(request, 'info.html', {'book': book})

def book_detail(request, book_id):
    book = get_object_or_404(Books, pk=book_id)

    borrow_requested = BorrowRequest.objects.filter(book=book, requested_by=request.user).exists()

    # Retrieve borrow_message from query parameters
    borrow_message = request.GET.get('borrow_message', "")

    context = {
        'book': book,
        'borrow_requested': borrow_requested,
        'borrow_message': borrow_message,
    }

    return render(request, 'info.html', context)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseNotFound
from librarian.models import Books, ApprovedRequest

def prev_file(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    
    # Increment page views
    Books.objects.filter(pk=book_id).update(PageViews=F('PageViews') + 1)
    
    # Check if the file exists
    if not book.BookFile:
        return HttpResponseNotFound('File not found')
    
    # Bypass authentication and permission checks if the book is an eBook
    if book.eBook:
        context = {
            'book': book,
        }
        return render(request, 'prev.html', context)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You need to be logged in to access this book.")
    
    # Check if there exists an approved request for the book and user
    if ApprovedRequest.objects.filter(book=book, requested_by=request.user).exists():
        context = {
            'book': book,
        }
        return render(request, 'prev.html', context)
    else:
        return HttpResponseForbidden("You don't have permission to access this book.")

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) >= 3:
        books = Books.objects.filter(BookTitle__icontains=query) | Books.objects.filter(Author__icontains=query)
        suggestions = [
            {
                'id': book.id,
                'title': book.BookTitle,
                'author': book.Author,
                'description': book.Description,
                'date': book.Date.strftime('%Y-%m-%d'),
                'category': ', '.join(category.name for category in book.Category.all()),
                'language': book.Language,
                'image_url': book.BookImage.url,
                'views': book.PageViews,
                'available': book.available
            }
            for book in books
        ]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)

@login_required
def bookmark(request):
    # Filter books that are bookmarked by the current user
    bookmarked_books = Books.objects.filter(bookmarked_by=request.user)
    return render(request, 'bookmark_content.html', {'all_books': bookmarked_books})

@login_required
def bookmark_status(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    bookmarked = request.user in book.bookmarked_by.all()
    return JsonResponse({'bookmarked': bookmarked})

@login_required
def unbookmark_all(request):
    if request.method == 'POST':
        user = request.user
        try:
            user.bookmarks.clear()  # Clear the bookmarks correctly
            return JsonResponse({'success': True})
        except Exception as e:
            logging.error(f"Error unbookmarking all books for user {user.id}: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
@login_required
def bookmark_toggle(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Books, pk=book_id)
        user = request.user

        if user in book.bookmarked_by.all():
            book.bookmarked_by.remove(user)
            bookmarked = False
        else:
            book.bookmarked_by.add(user)
            bookmarked = True

        return JsonResponse({'bookmarked': bookmarked})
    return JsonResponse({'error': 'Invalid request'})

@login_required
def borrow_request(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    user = request.user

    borrow_requested = BorrowRequest.objects.filter(book=book, requested_by=user).exists()

    if book.available and not borrow_requested:
        BorrowRequest.objects.create(book=book, requested_by=user)
        messages.success(request, "Your request to borrow this book has been submitted.")
    elif borrow_requested:
        messages.info(request, "You have already requested to borrow this book.")
    else:
        messages.error(request, "This book is not available for borrowing.")

    return redirect(reverse('view'))

@login_required
def request_history_view(request):
    pending_requests = BorrowRequest.objects.filter(requested_by=request.user)
    for request_obj in pending_requests:
        if request_obj.is_expired() and request_obj.status != 'Expired':
            request_obj.status = 'Expired'
            request_obj.save()

    approved_requests = ApprovedRequest.objects.filter(requested_by=request.user)
    declined_requests = DeclinedRequest.objects.filter(requested_by=request.user)

    context = {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'declined_requests': declined_requests,
    }

    return render(request, 'requesthistory.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, ("You were Logged Out!"))
    url = reverse('login_user')
    return redirect (url)