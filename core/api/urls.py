from django.urls import path
from knox import views as knox_views

from . import views

app_name = "api"

urlpatterns = [
    path("", views.OverviewAPI.as_view(), name="overview"),
    path("login/", views.LoginAPI.as_view(), name="login"),
        # logout user
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    # logout user from all sessions
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
