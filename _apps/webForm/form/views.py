import json
from telegram.variables import bot_domain, external_web_hook, server_domain, endpoint_form, form_page

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response

# from telegram.telegram_bot import BotHandlers
from .forms import FormForms
from .models import *
from .serializers import FormSerializer

def home(request):
  return render(request, 'home.html', {'server_domain': server_domain, 'endpoint_form': endpoint_form})

def form_is_completed(request):
  return render(request, 'form_is_completed.html', {'server_domain': server_domain, 'endpoint_form': endpoint_form})

class webFormView(generics.ListCreateAPIView, generics.ListAPIView):
  queryset = webFormModel
  serializer_class = FormSerializer

  def post(self, request, *args, **kwargs):
    selected_values = request.POST.getlist('optimalInvestmentPeriod')
    print(selected_values)
    selected_values = selected_values[:-1] if selected_values and not selected_values[-1] else selected_values
    if not selected_values or not selected_values[0]:
      return HttpResponse("<script>alert('You did not check the checkboxes');</script>")
    else:
      pass

    json_data = json.dumps(selected_values)
    data = request.data.dict()
    data['optimalInvestmentPeriod'] = json_data
    form = FormForms(data)
    if form.is_valid():
      serializer = self.get_serializer(data=data)
      if serializer.is_valid(raise_exception=True):
        pass
      # self.create_object(data)
      serializer.save()
      path = bot_domain + external_web_hook
      serializer_data = dict(serializer.data)
      response = requests.post(path, json=serializer_data)
      if 200 >=response.status_code < 300:
        # return Response({"message": "Data was saved"})
        return redirect(server_domain + "form_is_completed/")

        # return render(request, "form_is_completed.html", {'server_domain': server_domain, 'endpoint_form': endpoint_form})
    return Response({"message": "Data wasn't saved"})

  def get(self, request, *args, **kwargs):
    queryset = webFormModel.objects.all()
    serializer = self.get_serializer(queryset, many=True)
    return Response({"response": serializer.data})

  # def create_object(self, validated_data):
  #   return webFormModel.objects.using('default').create(**validated_data)

