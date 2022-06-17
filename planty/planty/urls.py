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
from django.conf import settings
from django.conf.urls.static import static
from posts.views import (NewPostView, PostDetailView,
                         UpdatePostView, DeletePostView)


urlpatterns = [
    path('', main_views.homepage, name="homepage"),
    path('register/', user_views.register, name="register"),
    # 'template_name' = name of custom template
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name="login"),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name="logout"),
    path('profile/<int:pk>/',
         user_views.view_profile,
         name="view_profile"),
    path('profile/update/',
         user_views.update_profile,
         name="update_profile"),
    path('new-post/', NewPostView.as_view(), name='new_post'),
    path('post/<int:pk>/',
         PostDetailView.as_view(),
         name='post-detail'),
    path('post/<int:pk>/update/',
         UpdatePostView.as_view(),
         name='post-update'),
    path('post/<int:pk>/delete/',
         DeletePostView.as_view(),
         name='post-delete'),
]


# Allow media to work with browser - only in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
