from django.db.models import Q

from ..models import Vacancies
from ..serializers import VacanciesSerializerOLD

from rest_framework import viewsets, permissions


class VacancyToTGBotViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializerOLD
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Возвращение записей из бд с полученными фильтрами от запроса пользователя"""

        queryset = Vacancies.objects.all()

        query_params = self.request.query_params
        query_string = next(iter(query_params.keys()))
        params_list = query_string.split("&")
        parsed_params = {}

        for param in params_list:
            key, value = param.split("=", 1)
            parsed_params[key] = value

        direction_ = parsed_params.get("selected_direction", "")
        specialization_ = parsed_params.get("selected_specializations", "")[2:-2]
        level_ = parsed_params.get("selected_level", "")[2:-2]
        selected_location_ = parsed_params.get("selected_location", "")[2:-2]
        work_format_ = parsed_params.get("selected_work_format", "")[2:-2]
        keyword = parsed_params.get("keyword", "")
        interval = parsed_params.get("interval", "")

        level = level_.replace("'", "").strip()
        direction = direction_.replace("'", "").strip()
        specialization = specialization_.replace("'", "").strip()
        selected_location = selected_location_.replace("'", "").strip()
        work_format = work_format_.replace("'", "").strip()

        if level:
            level_conditions = Q()
            for word in level.split(", "):
                level_conditions |= Q(level__icontains=word)
            queryset = queryset.filter(level_conditions)

        if direction:
            direction_conditions = Q()
            for word in direction.split(", "):
                direction_conditions |= Q(profession__icontains=word)
            queryset = queryset.filter(direction_conditions)

        if work_format:
            work_format_conditions = Q()
            for word in work_format.split(", "):
                work_format_conditions |= Q(job_type__icontains=word)
            queryset = queryset.filter(work_format_conditions)

        if specialization:
            specialization_conditions = Q()
            for word in specialization.split(", "):
                specialization_conditions |= Q(body__icontains=word)
            queryset = queryset.filter(specialization_conditions)

        if keyword:
            keyword_conditions = Q()
            for word in keyword.split(", "):
                keyword_conditions |= Q(body__icontains=word)
            queryset = queryset.filter(keyword_conditions)
        if interval:
            pass
        return queryset
