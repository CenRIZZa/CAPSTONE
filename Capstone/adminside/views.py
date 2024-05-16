from django.shortcuts import render
from librarian.models import Books
# Create your views here.
def adminPage(request):

   return render(request,'admin.html', {})


def book_page_views(request):
    # Retrieve all books and sort them by page views in descending order
    books = Books.objects.all().order_by('-PageViews')[:7]

    # Extract book titles and page views
    book_titles = [book.BookTitle for book in books]
    page_views = [book.PageViews for book in books]

    # Render the template with the necessary data
    return render(request, 'book_page_views.html', {'book_titles': book_titles, 'page_views': page_views})

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivity
import pytz # type: ignore

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Get the timezone object for Asia/Manila
    tz = pytz.timezone('Asia/Manila')
    # Get the current time in UTC
    login_time_utc = timezone.now()
    # Convert the UTC time to Philippine time
    login_time_ph = login_time_utc.astimezone(tz) + timezone.timedelta(hours=8)
    # Save the login time in the database
    UserActivity.objects.create(user=user, login_time=login_time_ph)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    # Get the timezone object for Asia/Manila
    tz = pytz.timezone('Asia/Manila')
    # Get the current time in UTC
    logout_time_utc = timezone.now()
    # Convert the UTC time to Philippine time
    logout_time_ph = logout_time_utc.astimezone(tz) + timezone.timedelta(hours=8)
    # Retrieve the last activity for the user
    last_activity = UserActivity.objects.filter(user=user).order_by('-login_time').first()
    if last_activity:
        # Update the logout time for the last activity
        last_activity.logout_time = logout_time_ph
        last_activity.save()

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivity

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Set UserActivity instances as active upon login
    UserActivity.objects.filter(user=user, active=False).update(active=True)
    print("ACTIVE")

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    # Set UserActivity instances as inactive upon logout
    UserActivity.objects.filter(user=user, active=True).update(active=False)
    print("NOT ACTIVE")