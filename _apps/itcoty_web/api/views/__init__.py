from .google_auth import GoogleLoginView, UserRedirectView
from .profile import ProfileViewSet
from .vacancies import AllVacanciesView, ThreeVacanciesView, VacanciesViewSet, VacanciesViewSetOLD
from .user_requests_from_tg_individ_bot import UserRequestsViewSet
from .vacancy_to_tg_individ_bot import VacancyToTGBotViewSet
from .registration import CustomVerifyEmailView

__all__ = [
    "GoogleLoginView",
    "UserRedirectView",
    "AllVacanciesView",
    "VacanciesViewSet",
    "ThreeVacanciesView",
    "ProfileViewSet",
    "VacanciesViewSetOLD",
    "UserRequestsViewSet",
    "VacancyToTGBotViewSet",
    "CustomVerifyEmailView",
]
