from django.contrib import admin
from .models import Themes
from .models import Themes, Comments, Counselors
# Register your models here.
admin.site.register(Themes)
admin.site.register(Comments)
admin.site.register(Counselors)