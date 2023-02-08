from django.urls import path
from users.views import UserView
from roles.views import RoleView
from learning_style.views import LearningStyleView
from Auth.views import AuthView,LogOutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users', UserView.as_view()),
    path('roles', RoleView.as_view()),
    path('learning_styles', LearningStyleView.as_view()),
    path('login', AuthView.as_view()),
    path('logout', LogOutView.as_view()),
    path('refresh', TokenRefreshView.as_view())
]
