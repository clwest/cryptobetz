
from django.contrib import admin
from .models import Coindesk



# Admin.register() decorator



# admin.site.register(Category)
admin.site.register(Coindesk)





admin.site.site_header = "Donkey Betz Admin"
