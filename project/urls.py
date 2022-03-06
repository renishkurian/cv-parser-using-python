from django.urls import path
from . import views
urlpatterns=[
    path('',views.Projects.as_view(),name='project'),
    path('show/<int:pk>',views.ProjectInfo.as_view(),name='view shelves'),
    path('new',views.CreateNewProject.as_view(),name='createproject'),
    path('delete',views.delete),
    path('folder_color', views.folder_color),
    path('newfilter',views.create_bucket,name='createbucket'),
    path('get_bucket',views.get_bucket,name='fetch-bucket')

]