from django.urls import path 
from .views import NotesViewSet
  
urlpatterns = [ 
    path("", NotesViewSet.as_view({'get': 'list', 'post': 'create'}), name="get-create-notes"),
    path("<int:pk>/", NotesViewSet.as_view({'get': 'list', 'put': 'update', 'delete': 'destroy'}), name="get-note"),
    path("<int:pk>/share/", NotesViewSet.as_view({'post': 'create'}), name="share-note"),
] 