"""Contains the urls for the form_creator app"""
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(
    "get_diagram_user_stories",
    views.GetDiagramUserStoriesViewSet,
    "get_diagram_user_stories",
)

urlpatterns = [
    path("", include(router.urls)),
    path('add', views.add_diagram, name='add_diagram'),
    path('replace/<int:diagram_id>', views.replace_diagram, name='replace_diagram'),
    path('get/<int:diagram_id>', views.get_diagram, name='get_diagram_manticore'),
    path('delete/<int:diagram_id>', views.delete_diagram, name='delete_diagram'),
    path('delete_bulk', views.delete_bulk_diagram, name='delete_bulk_diagram'),
    path('data_list', views.list_diagram, name='data_list_diagram'),
    path('diagram_to_us/<int:diagram_id>', views.diagram_to_us, name='diagram_to_us'),
    # path('get_diagram_user_stories/<int:diagram_id>', views.GetDiagramUserStoriesViewSet, name='get_diagram_user_stories'),
]
