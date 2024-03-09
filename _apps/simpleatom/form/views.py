from django.forms import model_to_dict
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .variables import variables
from .serializers import *
from .models import *

def home_page_view(request):
    return render(request, 'home_oldform.html')


class FormDataView(generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView):

    serializer_class = FormDataSerializer
    queryset = FormAnswerModel.objects.all()

    def post(self, request, *args, **kwargs):
        updated_data = self.update_data(request_data=request.data)
        return self.create(updated_data, *args, **kwargs)

    def create(self, updated_data, *args, **kwargs):
        serializer = self.get_serializer(data=updated_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update_data(self, request_data):
        updated_data = {}
        self.fields = self.model_fields(model=FormAnswerModel)
        for key in request_data:
            if key in self.fields:
                updated_data[key] = request_data[key]
            # else:
            if not updated_data.get(variables.common_field_name):
                updated_data[variables.common_field_name] = {}
            updated_data[variables.common_field_name][key] = request_data[key]
        # print(updated_data)
        return updated_data

    def patch(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        instance = FormAnswerModel.objects.get(id=id)
        instance_data = model_to_dict(instance)
        updated_data = self.updated_dict(request_data=request.data, instance_data=instance_data)

        if updated_data:
            kwargs['partial'] = True
            return self.update(updated_data, *args, **kwargs)
        return Response({"message": "the same data"})

    def update(self, updated_data, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=updated_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def model_fields(self, model):
        model_meta = model._meta
        fields = model_meta.get_fields()
        fields = [i.attname for i in fields]
        if 'id' in fields:
            fields.remove('id')
        return fields

    def updated_dict(self, request_data, instance_data):
        try:
            instance_data.pop('id')
        except Exception as ex:
            print(ex)
        """
        3 scenario:
        0) email and data keys have been received the same time
        1) keys don't match -
        2) part of keys don't match
        3) all keys match
        """
        updated_data = self.update_data(request_data)
        # print('updated |', updated_data)
        # print('instance|', instance_data)
        # common_keys = set(updated_data.keys()) & set(instance_data.keys())

        for key in updated_data:
            if key == variables.common_field_name:
                for second_key in updated_data[variables.common_field_name]:
                    if not instance_data.get(variables.common_field_name):
                        instance_data[variables.common_field_name] = {}
                    instance_data[variables.common_field_name][second_key] = self.compare_data(instance_data[variables.common_field_name], updated_data[variables.common_field_name], second_key)
            else:
                instance_data[key] = self.compare_data(instance_data, updated_data, key)
        return instance_data

    def compare_data(self, instance_data_key, updated_data_key, second_key):
        if not instance_data_key.get(second_key):
            return updated_data_key[second_key]

        if instance_data_key[second_key] != updated_data_key[second_key]:
            return updated_data_key[second_key]
        return instance_data_key[second_key]

    def get(self, request, *args, **kwargs):
        email = request.query_params['email'] if request.query_params.get('email') else None
        if not email:
            return self.list(request, *args, **kwargs)
        else:
            queryset = FormAnswerModel.objects.filter(email=email)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class QuestionsView(generics.CreateAPIView, generics.UpdateAPIView, generics.ListAPIView):
    serializer_class = CustomFormSerializer
    queryset = CustomFormModel.objects.all()

    def get(self, request, *args, **kwargs):
        if request.query_params.get('form_name'):
            queryset =  CustomFormModel.objects.filter(form_name=request.query_params['form_name'])
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return self.list(request, *args, **kwargs)

