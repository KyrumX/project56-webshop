from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.ChatboxView.as_view(), name="chatbot"),
    url(r'^GetBotResponse.py$', views.GetBotResponse, name='login'),
]
