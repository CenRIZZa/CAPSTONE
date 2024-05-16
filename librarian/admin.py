from django.contrib import admin

# Register your models here.
from .models import Books, Category, BorrowRequest
# Register your models here.
admin.site.register(Books)
admin.site.register(Category)
admin.site.register(BorrowRequest)
