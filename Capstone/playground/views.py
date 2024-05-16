from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseNotFound
from .models import Brgy
from librarian.models import Books

import json

# Create your views here.
def say_hello(request):
   all_books = Books.objects.all
   return render(request,'index.html', {'all': all_books})

def join(request):
   all_brgy = Brgy.objects.all
   return render(request,'join.html', {'all': all_brgy})






def search_books(request):
    query = request.GET.get('query')
    filter_by = request.GET.get('filter')
    if filter_by == 'title':
        # Search for books by title
        books = Books.objects.filter(BookTitle__icontains=query)
        # Redirect to the book page if only one book matches the query
        if books.count() == 1:
            book = books.first()
            return redirect('book_detail', book_id=book.id)
    # Handle other search filters and scenarios here
    return render(request, 'search_results.html', {'books': books})

def book_detail(request, book_id):
    # Retrieve the book object with the specified ID, or return a 404 error page if not found
    book = get_object_or_404(Books, pk=book_id) 
    
    return render(request, 'book_detail.html', {'book': book})

#hindi pa gumagana login
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Redirecting to home...")
            return redirect('home')  # Redirect to home page after successful login
        else:
            print("Login failed.")
            # Return an error message or handle the failed login attempt
            pass  # Add your logic here
    return render(request, 'login.html')



#pang RECENTLY DELETED


