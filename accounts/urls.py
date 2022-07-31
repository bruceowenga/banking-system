from . import views
from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView, editProfile, AttendanceView


app_name = 'accounts'

urlpatterns = [
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    path(
        "profile/", views.editProfile,
        name="edit_profile"
    ),
    path(
        "attendance/", AttendanceView.as_view(), 
        name="attendance"
    )
]
