from django.conf.urls import url

from . import views

urlpatterns = [
    url('^callback/', views.callback),
    url('^map/', views.map)
]
