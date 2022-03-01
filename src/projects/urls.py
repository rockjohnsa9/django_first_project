from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.projects, name="projects"),
    path('projects/<str:pk>/', view=views.project, name="project"),
    path('create-project/', view=views.createProject, name="create-project"),
    path('update-project/<str:pk>/',
         view=views.updateProject, name='update-project'),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),
]
