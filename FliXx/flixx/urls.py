"""FliXx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/',views.login,name='login'),
    url(r'^$', views.home,name='home'),
    url(r'^(\d{1,4})$', views.detailedview, name='detailedview'),
    url(r'^(\d{1,4})/(\d{1})$', views.lik ,name='like'),
    url(r'^recommend/$', views.recommend, name='recommend'),
    url(r'^watched-movies/$', views.watchedmovies ,name='watched-movies'),
    url(r'^aboutus/$', views.about_us , name='about us'),
    url(r'^Xplore/$',views.find,name='search')
]