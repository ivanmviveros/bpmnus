"""Views for the projects module"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from projects.business_logic import data_filters
from projects.business_logic.data_alter import before_save_project, before_update_project

from .models import Projects
from .serializers import ProjectsSerializer

@api_view(['POST'])
def add_project(request):
    """Tries to create a project and returns the result"""
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.add(request, before_save_project)

@api_view(['PUT'])
def replace_project(request, project_id):
    "Tries to update a project and returns the result"
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.replace(request, project_id, before_update_project(project_id))

@api_view(['GET'])
def get_project(request, project_id):
    "Return a JSON response with project data for the given id"
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.get(request, project_id)

@api_view(['DELETE'])
def delete_project(request, project_id):
    """Tries to delete an project and returns the result."""
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.delete(project_id, "Proyecto elminado exitosamente")

@api_view(['DELETE'])
def delete_bulk_project(request):
    """Tries to delete an project and returns the result."""
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.delete_bulk(request)

@api_view(['POST', 'OPTIONS'])
def list_project(request):
    """Returns a JSON response containing registered project for a datatable"""
    crud_object = Crud(ProjectsSerializer, Projects)
    return crud_object.listing(request, data_filters.project_listing_filter)
