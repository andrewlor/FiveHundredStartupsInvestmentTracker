"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^auth$', views.auth),
    url(r'^$', views.index),

    url(r'^newperson$', views.newperson),
    url(r'^createperson$', views.createperson),
    url(r'^editperson/(\d+)$', views.editperson),

    url(r'^vote/(\d+)$', views.vote),

    url(r'^newcompany$', views.newcompany),
    url(r'^createcompany$', views.createcompany),
    url(r'^editcompany/(\d+)$', views.editcompany),


    url(r'^newvote$', views.newvote),
    url(r'^createvote$', views.createvote),

    url(r'^newentry$', views.newentry),
    url(r'^createentry$', views.createentry),

    url(r'^data$', views.data)
]
