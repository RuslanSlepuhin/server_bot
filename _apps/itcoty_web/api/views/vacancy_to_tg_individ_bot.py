from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from ..models import Vacancies
from ..serializers import VacanciesSerializerOLD

from rest_framework import viewsets, permissions

from ..tg_bot_logics.get_filtered_params import GetFilteredParams
from ..tg_bot_logics.get_queryset import GetQuerysetToTGBot
from ..tg_bot_logics.get_request_params import GetRequestParams


class StandardResultsSetPagination(PageNumberPagination):
    """resizable pagination"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class VacancyToTGBotViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializerOLD
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Возвращение записей из бд с полученными фильтрами от запроса пользователя"""

        queryset_ = Vacancies.objects.all()
        parsed_params = GetRequestParams.get_request_params(self.request.query_params)
        filtered_tuple = GetFilteredParams.get_filtered_params(parsed_params)
        queryset = GetQuerysetToTGBot.get_tg_queryset(queryset_, *filtered_tuple)
        return queryset

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
