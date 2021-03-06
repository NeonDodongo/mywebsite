"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
# string path, regex path
from django.urls import path, re_path

from forum import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^forum/$', views.forum, name='forum'),
    re_path(r'^forum/(?P<pk>\d+)/$', views.forum_topics, name='forum_topics'),
    re_path(r'^forum/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    re_path(r'^admin/', admin.site.urls),
]
