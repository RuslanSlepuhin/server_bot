from django.utils.translation import gettext_lazy as _
from django_countries import Countries


class ProfileCountries(Countries):
    only = ["BY", "RU", "UA", "FR", "DE", "PL", "CN", "LT", "LV", ("OT", _("Other"))]
