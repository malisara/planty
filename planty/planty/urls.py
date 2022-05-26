"""planty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views as main_views
from users import views as user_views
from django.contrib.auth import views as auth_views

# TODO: Logout

urlpatterns = [
    path('', main_views.homepage, name="homepage"),
    path('register/', user_views.register, name="register"),
    # Template_name = where dj searches for the template
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
]
