from django.db.models import QuerySet, Q


class GetQuerysetToTGBot:
    @staticmethod
    def get_tg_queryset(
        queryset: QuerySet,
        level: str,
        direction: str,
        work_format: str,
        specialization: str,
        keyword: str,
    ) -> QuerySet:

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

        return queryset
