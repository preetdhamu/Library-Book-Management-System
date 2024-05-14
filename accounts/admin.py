from django.contrib import admin

# Register your models here.
from .models import Profile,Book,IssuedBook,Chat
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(IssuedBook)
admin.site.register(Chat)