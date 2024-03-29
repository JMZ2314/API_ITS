from django.urls import path
from users.views import UserView,RegisterView
from roles.views import RoleView
from lessons.views import LessonView
from sections.views import SectionView
from tests.views import TestView
from types_test.views import TypeTestView
from answers.views import AnswerView
from levels_test.views import LevelTestView
from learning_style.views import LearningStyleView
from courses.views import CourseView
from Auth.views import AuthView,LogOutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users', UserView.as_view()),
    path('roles', RoleView.as_view()),
    path('lessons', LessonView.as_view()),
    path('courses', CourseView.as_view()),
    path('sections', SectionView.as_view()),
    path('tests', TestView.as_view()),
    path('answers', AnswerView.as_view()),
    path('types_test', TypeTestView.as_view()),
    path('levels_test', LevelTestView.as_view()),
    path('learning_styles', LearningStyleView.as_view()),
    path('login', AuthView.as_view()),
    path('logout', LogOutView.as_view()),
    path('signin', RegisterView.as_view()),
    path('refresh', TokenRefreshView.as_view())
]
