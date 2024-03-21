import django_filters

from .models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    start_id = django_filters.NumberFilter(field_name="id", lookup_expr="lt")

    class Meta:
        model = Vacancy
        fields = ["start_id"]
