from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (AllVacanciesView, GoogleLoginView, ThreeVacanciesView,
                    UserRedirectView, VacanciesViewSet)

router = SimpleRouter()
router.register("vacancies", VacanciesViewSet, basename="vacancy")

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("get-all-vacancies/", view=AllVacanciesView.as_view(), name="all_vacancies"),
    path(
        "three-last-vacancies/",
        view=ThreeVacanciesView.as_view(),
        name="three_vacancies",
    ),
]

urlpatterns += router.urls
