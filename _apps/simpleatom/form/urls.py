from django.urls import path
from .views import *

urlpatterns = [
    path('form_data/<int:pk>/', FormDataView.as_view()),
    path('form_data/', FormDataView.as_view()),
    path('form_data/<slug:parameter>/', FormDataView.as_view()),

    path('questions/', QuestionsView.as_view()),

    path('home/', home_page_view),

]
