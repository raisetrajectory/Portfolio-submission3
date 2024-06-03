from django.contrib import admin
from .models import User, Counselor, CounselingSession, ChatMessage, Task

# from django.contrib import admin
# from .models import CustomUser, Counselor, CounselingSession, ChatMessage, Task

# Register your models here.
# admin.site.register(CustomUser)
admin.site.register(User)
admin.site.register(Counselor)
admin.site.register(CounselingSession)
admin.site.register(ChatMessage)
admin.site.register(Task)
