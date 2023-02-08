from django.contrib import admin
from core.models import User,Role,LearningStyle,Module,Operation

admin.site.register(User)
admin.site.register(Role)
admin.site.register(LearningStyle)
admin.site.register(Module)
admin.site.register(Operation)

