from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import NFTS



# Admin.register() decorator



# admin.site.register(Category)
admin.site.register(NFTS)





admin.site.site_header = "Donkey Betz Admin"