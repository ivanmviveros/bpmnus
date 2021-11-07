"""Standard functions for crud"""
from rest_framework import status
from rest_framework.response import Response
from core.crud.exeptions import NonCallableParam

class Crud():
    """Manages the standard functions for crud in modules"""

    def __init__(self, serializer_class, model_class):
        self.serializer_class = serializer_class
        self.model_class = model_class

    def save_instance(self, data, request=None, identifier=0, after_save=None):
        """Saves a model intance"""
        if identifier:
            model_obj = self.model_class.objects.get(pk=identifier)
            data_serializer = self.serializer_class(model_obj, data=data)

        else:
            data_serializer = self.serializer_class(data=data)
        if data_serializer.is_valid():
            model_obj = data_serializer.save()
            if Crud.validate_function(after_save):
                after_save(request, data_serializer)
            return {"success": True, "id": model_obj.pk}, status.HTTP_201_CREATED

        answer = self.error_data(data_serializer)
        return answer, status.HTTP_400_BAD_REQUEST

    def add(self, request, before_add=None):
        """Tries to create a row in the database and returns the result"""
        if Crud.validate_function(before_add):
            data = before_add(request.data.copy())
        answer, answer_status = self.save_instance(data, request)
        return Response(
            answer,
            status=answer_status,
            content_type='application/json'
        )

    def replace(self, request, identifier, before_replace=None):
        """Tries to update a row in the db and returns the result"""    
        if Crud.validate_function(before_replace):
            data = before_replace(request.data.copy())
        answer, answer_status =  self.save_instance(data, request, identifier)
        return Response(
            answer,
            status=answer_status,
            content_type='application/json'
        )

    def get(self, request, identifier, alter_model=None, alter_return=None):
        """Return a JSON response with data for the given id"""
        try:
            model_obj = self.model_class.objects.get(pk=identifier)
            data_serializer = self.serializer_class(model_obj)
            model_data = data_serializer.data.copy()
            if Crud.validate_function(alter_model):
                model_data = alter_model(model_data)

            data = {
                "success": True,
                "data": model_data
            }

            if Crud.validate_function(alter_return):
                data = alter_return(request, data)

            return Response(
                data,
                status=status.HTTP_200_OK,
                content_type='application/json'
            )
        except self.model_class.DoesNotExist:
            data = {
                "success": False,
                "error": "No existe el registro, quiza haya sido borrado hace poco"
            }
            return Response(
                data,
                status=status.HTTP_404_NOT_FOUND,
                content_type='application/json'
            )

    def delete(self, identifier, message):
        """Tries to delete a row from db and returns the result"""
        model_obj = self.model_class.objects.get(id=identifier)
        model_obj.delete()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def toggle(self, identifier, data_name):
        """Toogles the active state for a given row"""
        model_obj = self.model_class.objects.get(id=identifier)
        previous = model_obj.active

        if previous:
            message = data_name + " desactivado con exito"
        else:
            message = data_name + " activado con exito"

        model_obj.active = not model_obj.active
        model_obj.save()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def picker_search(self, request, filter_function):
        """Returns a JSON response with data for a selectpicker."""
        value = request.data['value']
        queryset = filter_function(value)
        serializer = self.serializer_class(queryset, many=True)
        result = serializer.data
        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    def listing(self, request, listing_filter):
        """ Returns a JSON response containing registered users"""
        sent_data = request.data
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        search = sent_data['search[value]']

        records_total = self.model_class.objects.count()

        if search != '':
            queryset = listing_filter(search, start, length)
            records_filtered = listing_filter(search, start, length, True)
        else:
            queryset = self.model_class.objects.all()[start:start + length]
            records_filtered = records_total

        result = self.serializer_class(queryset, many=True)
        data = {
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': result.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    @staticmethod
    def error_data(serializer):
        """Return a common JSON error result"""
        error_details = []
        for key in serializer.errors.keys():
            error_details.append(
                {"field": key, "message": serializer.errors[key][0]})

        data = {
            "succes": False,
            "Error": {
                "success": False,
                "status": 400,
                "message": "Los datos enviados no son validos",
                "details": error_details
            }
        }
        return data

    @staticmethod
    def validate_function(f):
        """Checks if the given parameter is a function"""
        if f is None:
            return False
        if callable(f):
            return True
        raise NonCallableParam
