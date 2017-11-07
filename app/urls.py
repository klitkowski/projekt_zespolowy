"""systemsm URL Configuration

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
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^add/event/$', views.add_event, name='add_event'),
    url(r'^ticket/(?P<ticket_id>[0-9]+)/$', views.ticket, name='ticket'),
    url(r'^tickets/$', views.tickets, name='tickets'),
    url(r'^add/ticket/$', views.add_ticket, name='add_ticket'),
]
