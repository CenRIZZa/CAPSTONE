from django.contrib import admin

# Register your models here.
from .models import Books, Category, BorrowRequest,ApprovedRequest,DeclinedRequest, SubCategory
# Register your models here.
admin.site.register(Books)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BorrowRequest)
admin.site.register(ApprovedRequest)
admin.site.register(DeclinedRequest)