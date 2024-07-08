from django.contrib import admin

from .models import Users #不要となった場合は削除して大丈夫です
# Register your models here.
admin.site.register(Users) #不要となった場合は削除して大丈夫です

# from django.contrib import Counselor
from .models import Counselor #不要となった場合は削除して大丈夫です
admin.site.register(Counselor) #不要となった場合は削除して大丈夫です