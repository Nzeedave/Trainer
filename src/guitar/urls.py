from django.conf.urls import patterns, url
from guitar import views

urlpatterns = patterns('',
    url(r'^select_exercise/$', views.select_exercise, name="select_exercise"),
    url(r'^exercise/(?P<exercise_id>[\w\-]+)', views.exercise, name="exercise"),
    url(r'select_routine/$', views.select_routine, name="select_routine"),
    url(r'^routine/(?P<routine_slug>[\w\-]+)/$', views.show_routine, name="show_routine"),
    url(r'^routine/(?P<routine_slug>[\w\-]+)/(?P<item_id>[\d]+)/$', views.routine_exercise, name="routine_exercise"),
    url(r'^routine/(?P<routine_slug>[\w\-]+)/finish/$', views.routine_finish, name='routine_finish'),
    url(r'^routine/(?P<routine_slug>[\w\-]+)/abort/$', views.routine_abort, name='routine_abort'),    
    url(r'^test/$', views.test, name="test"),
    
    )