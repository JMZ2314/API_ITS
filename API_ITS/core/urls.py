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
from answer_user.views import AnswerUserView
from courses.views import CourseView,CourseViewDetail
from Auth.views import AuthView,LogOutView
from resource.views import ResourceView
from rest_framework_simplejwt.views import TokenRefreshView
from progress.views import ProgressView
from suggestions.views import SuggestionView,SuggestionViewDetail

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
    path('answer_user', AnswerUserView.as_view()),
    path('resources', ResourceView.as_view()),
    path('login', AuthView.as_view()),
    path('logout', LogOutView.as_view()),
    path('signin', RegisterView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('progress', ProgressView.as_view()),
    path('suggestions', SuggestionView.as_view()),
    path('suggestions/<int:pk>', SuggestionViewDetail.as_view()),
    path('suggestions/<int:pk>', SuggestionViewDetail.as_view()),
    path('courses/<int:pk>', CourseViewDetail.as_view()),
]
