from django.contrib import admin
from .models import Category
from .models import Rating

# Register your models here.
admin.site.register(Category)
admin.site.register(Rating)
