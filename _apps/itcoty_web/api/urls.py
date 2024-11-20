from django.urls import path, re_path
from django.conf.urls import include

from dj_rest_auth.registration.views import VerifyEmailView
from rest_framework.routers import SimpleRouter
from .views import (
    AllVacanciesView,
    ProfileViewSet,
    ThreeVacanciesView,
    VacanciesViewSet,
    VacanciesViewSetOLD,
    UserRequestsViewSet,
    VacancyToTGBotViewSet,
    GoogleLoginView,
    UserRedirectView,
)

router = SimpleRouter()
router.register("vacancies", VacanciesViewSet, basename="vacancy")
router.register("profile", ProfileViewSet, basename="profile")
router.register(
    'users_requests',
    UserRequestsViewSet,
    basename="users_requests"
)
router.register(
    'vacancy_to_tg',
    VacancyToTGBotViewSet,
    basename="vacancy_to_tg"
)

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    re_path(
            r"^verify_email/(?P<key>[-:\w]+)/$",
            VerifyEmailView.as_view(),
            name="account_confirm_email"),
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path(
        "get-all-vacancies/",
        view=AllVacanciesView.as_view(),
        name="all_vacancies"
    ),
    path(
        "old-vacancies/",
        view=VacanciesViewSetOLD.as_view(),
        name="aoll_vacancies"
    ),
    path(
        "three-last-vacancies/",
        view=ThreeVacanciesView.as_view(),
        name="three_vacancies",
    ),
]

urlpatterns += router.urls
