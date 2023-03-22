from django.contrib import admin
from roles.models import Role
from learning_style.models import LearningStyle
from  types_test.models import TypeTest
from levels_test.models import LevelTest
from tests.models import Test
from answers.models import Answer,User_Answer
from courses.models import Course
from sections.models import Section
from lessons.models import Lesson
from modules.models import Module
from operations.models import Operation
from resource.models import Resource
from users.models import User



admin.site.register(User)
admin.site.register(Role)
admin.site.register(LearningStyle)
admin.site.register(Module)
admin.site.register(Operation)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Answer)

