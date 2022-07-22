"""Views for the diagrams module"""
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet

from core.crud.standard import Crud
from diagrams.business_logic import data_filters
from diagrams.business_logic.data_alter import add_request_files
from diagrams.business_logic.transform_xml import has_participants
from .models import Diagrams, UserStory
from .serializers import DiagramsSerializer, UserStorySerializer


@api_view(['POST'])
def add_diagram(request):
    """Tries to create a diagram and returns the result"""
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.add(request, add_request_files(request))

@api_view(['PUT'])
def replace_diagram(request, diagram_id):
    "Tries to update a diagram and returns the result"
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.replace(request, diagram_id, add_request_files(request))

@api_view(['GET'])
def get_diagram(request, diagram_id):
    "Return a JSON response with diagram data for the given id"
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.get(request, diagram_id)

@api_view(['DELETE'])
def delete_diagram(request, diagram_id):
    """Tries to delete an diagram and returns the result."""
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.delete(diagram_id, "Proyecto elminado exitosamente")

@api_view(['DELETE'])
def delete_bulk_diagram(request):
    """Tries to delete an diagram and returns the result."""
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.delete_bulk(request)

@api_view(['POST', 'OPTIONS'])
def list_diagram(request):
    """Returns a JSON response containing registered diagram for a datatable"""
    crud_object = Crud(DiagramsSerializer, Diagrams)
    return crud_object.listing(request, data_filters.diagram_listing_filter)

@api_view(['GET'])
def diagram_to_us(request, diagram_id):
    "Return a JSON response with diagram data for the given id"
    return has_participants(diagram_id)

class GetDiagramUserStoriesViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = UserStorySerializer

    def get_queryset(self):
        diagram_id = self.request.query_params.get("diagram_id")
        queryset = UserStory.objects.filter(diagram_id=diagram_id)
        return queryset
