from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Grocery)
admin.site.register(Author)
admin.site.register(Ingredient)
