from datetime import date, timedelta
from typing import Any

from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from ..filters import VacancyFilter
from ..helpers import add_numeration_to_response
from ..models import AdminVacancy, Vacancy
from ..serializers import AllVacanciesSerializer, VacanciesSerializer


class AllVacanciesView(generics.ListAPIView):
    queryset = AdminVacancy.objects.all()
    serializer_class = AllVacanciesSerializer
    permission_classes = [permissions.AllowAny]


class VacanciesViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = VacanciesSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VacancyFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        date_start = date.today() - timedelta(days=20)
        queryset = (
            Vacancy.objects.filter(created_at__gt=date_start).order_by("-id")
            # .distinct("id", "body") use in postgres only
        )
        return queryset

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().list(request, *args, **kwargs)
        data = (
            response.data
            if isinstance(response.data, list)
            else response.data.get("results", [])
        )
        new_response = {"vacancies": add_numeration_to_response(data)}

        return Response(new_response)


class ThreeVacanciesView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request) -> Response:
        trainees_vacancies = (
            Vacancy.objects.values(
                "id",
                "profession",
                "vacancy",
                "company",
                "job_type",
                "city",
                "salary",
                "created_at",
                "level",
                "salary_from_usd_month",
                "salary_to_usd_month",
            )
            .filter(level__icontains="trainee")
            .order_by("-id")[:3]
        )

        common_vacancies = (
            Vacancy.objects.values(
                "id",
                "profession",
                "vacancy",
                "company",
                "job_type",
                "city",
                "salary",
                "created_at",
                "level",
                "salary_from_usd_month",
                "salary_to_usd_month",
            )
            .exclude(level__icontains="trainee")
            .order_by("-id")[:3]
        )

        data = {
            "common_vacancies": add_numeration_to_response(common_vacancies),
            "vacancies": add_numeration_to_response(trainees_vacancies),
        }

        return Response(data)
