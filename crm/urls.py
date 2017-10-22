from crm import views
from django.conf.urls import url

urlpatterns = [
    url(r'^index.html$', views.index),
    url(r'^enrollment.html$', views.enrollment),
    url(r'^(\d+)/(\d+)/student_enrollment.html$', views.student_enrollment),
    url(r'', views.index),
]
