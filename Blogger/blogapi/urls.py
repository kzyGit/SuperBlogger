"""Blogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from .views.users import (UsersView, UserView, LoginView, LogoutView)

urlpatterns = [
    url(r'^users/', UsersView.as_view(), name="users"),
    url(r'^user/(?P<pk>[0-9]+)/', UserView.as_view(), name="user"),

    # Add login on browsable api
    url(r'^auth-api/', include('rest_framework.urls')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout')
]
