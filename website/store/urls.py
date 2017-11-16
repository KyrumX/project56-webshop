from django.conf.urls import url
from . import views #from currect package import...
from django.contrib.auth.views import login
urlpatterns = [

    url(r'^$', views.index, name='index'),
    # url(r'^$', login, {'template_name': 'index.html'}, name='index'),
    url(r'^login/$', views.loginview, name='login'),
    url(r'^register/$', views.register, name="register"),
    url(r'^contact/$', views.contact, name='contact'), #url = ip/contact/ of ip/contact (de eerste / is niet nodig)
    url(r'^faq$', views.faq, name='faq'),
    url(r'^about$', views.about, name='about'),
    url(r'^product/(?P<item>\d+)$', views.product, name='product2'), #url = /product/{item}, \d+ betekent 1 nummer of meer
	url(r'^search/(?P<query>[\w|\W]+)/$', views.search, name='search'),
    #url(r'^testing$', views.testing, name='testing'),
    url(r'^logout/$', views.logoutview, name='logout'),
    url(r'^registrationcomplete/$', views.registrationcomplete, name='regdone'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^messagesend/$', views.contactRequestHandeld, name='messagesend'),
    url(r'^result$', views.product, name='result'),
    url(r'^winkelwagentje/$', views.shoppingcart, name="shoppingcart"),
    url(r'^verlanglijst/$', views.wishlist, name="wishlist"),
    url(r'^processorder/$', views.processOrder, name="processorder"),
    url(r'^customerdetails/$', views.customerdetails, name="customerdetails"),
    url(r'^checkout/$', views.checkout, name="checkout"),
    url(r'^account/$', views.account, name="account"),
    url(r'^account/accountedit/$', views.accountedit, name="accountedit"),
    url(r'^account/changepassword/$', views.changepassword, name="changepassword")

]