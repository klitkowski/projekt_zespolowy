from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^ticket/(?P<ticket_id>[0-9]+)/$', views.ticket, name='ticket'),
    url(r'^invoice/(?P<invoice_id>[0-9]+)/$', views.invoice, name='invoice'),
    url(r'^invoice/pdf/(?P<invoice_id>[0-9]+)/$', views.pdf, name='pdf'),
    url(r'^tickets/$', views.tickets, name='tickets'),
    url(r'^invoices/$', views.invoices, name='invoices'),
    url(r'^issuers/$', views.issuers, name='issuers'),
    url(r'^owners/$', views.owners, name='owners'),
    url(r'^add/event/$', views.add_event, name='add_event'),
    url(r'^add/ticket/$', views.add_ticket, name='add_ticket'),
    url(r'^add/invoice/$', views.add_invoice, name='add_invoice'),
    url(r'^add/issuer/$', views.add_issuer, name='add_issuer'),
    url(r'^add/owner/$', views.add_owner, name='add_owner'),
    url(r'^delete/ticket/(?P<ticket_id>[0-9]+)/$', views.delete_ticket, name='delete_ticket'),
    url(r'^delete/event/(?P<event_id>[0-9]+)/$', views.delete_event, name='delete_event')
]
