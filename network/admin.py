from django.contrib import admin

from .models import User, AllPosts, followed, likes

# Register your models here.
admin.site.register(User)
admin.site.register(AllPosts)
admin.site.register(followed)
admin.site.register(likes)

# Register your models here.
