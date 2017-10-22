from django.conf.urls import url
from kingadmin import views

urlpatterns = [
    url(r'^admin.html$', views.admin),
    url(r'^(\w+)/(\w+)/$', views.show_model_table, name='show_model_table'),
    url(
        r'^(\w+)/(\w+)/(\d+)/change_data.html$',
        views.chang_data,
        name='table_obj_change', ),
    url(r'^(\w+)/(\w+)/add_data.html$', views.add_data),
    url(r'^(\w+)/(\w+)/(\d+)/delete_data.html$',
        views.delete_data,
        name='delete_data.html'),
]
