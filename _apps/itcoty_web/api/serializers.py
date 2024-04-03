from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .forms import CustomAllAuthPasswordResetForm
from .models import AdminVacancy, Vacancy

try:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import EmailAddress, SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
    from allauth.utils import get_username_max_length
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."),
            )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                _("The two password fields didn't match.")
            )
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm


class AllVacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminVacancy
        fields = [
            "id",
            "chat_name",
            "title",
            "body",
            "profession",
            "vacancy",
            "vacancy_url",
            "company",
            "english",
            "relocation",
            "job_type",
            "city",
            "salary",
            "experience",
            "contacts",
            "time_of_public",
            "created_at",
            "agregator_link",
            "session",
            "sended_to_agregator",
            "sub",
            "tags",
            "full_tags",
            "full_anti_tags",
            "short_session_numbers",
            "level",
            "approved",
            "salary_from",
            "salary_to",
            "salary_currency",
            "salary_period",
        ]


class VacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
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
