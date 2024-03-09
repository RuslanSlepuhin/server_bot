from rest_framework import serializers
from .models import *

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormAnswerModel
        fields = '__all__'

class CustomFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFormModel
        fields = '__all__'
