from django.contrib import admin

from .models import AdminVacancy, User, Vacancy


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
    )


@admin.register(AdminVacancy)
class AVacanciesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "vacancy_url",
        "company",
        "salary",
        "time_of_public",
        "created_at",
        "agregator_link",
    )
    list_display_links = ("id", "title")


@admin.register(Vacancy)
class VacanciesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "vacancy_url",
        "company",
        "salary",
        "time_of_public",
        "created_at",
        "agregator_link",
    )
    list_display_links = ("id", "title")
