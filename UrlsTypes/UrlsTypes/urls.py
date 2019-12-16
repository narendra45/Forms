"""UrlsTypes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView

from apptest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='home.html')),
    path('viewall/',views.viewAll,name='viewall'),
    path('viewdetails/<int:id>',views.viewDetails),
    path('partialupdate/',views.partialUpdate),
    path('update/',views.updateDetails,name='update'),#name field is mandatory for "{% url 'update' %}?id={{ x.id }}"
    path('delete/<int:id>',views.deleteDetails,name='delete'),#name field is mandatory for "{% url 'delete' x.id %}"
]
