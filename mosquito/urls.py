from django.conf.urls import url

from . import views

urlpatterns = [
    url('^callback/', views.callback),
    url('^map/', views.map),
    #url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT})
]
#urlpatterns += patterns('',(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)