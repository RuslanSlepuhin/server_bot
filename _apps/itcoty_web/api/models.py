from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []


class CurrentSession(models.Model):
    id = models.IntegerField(primary_key=True)
    session = models.CharField(max_length=15, unique=True)

    class Meta:
        managed = False
        db_table = "current_session"


class Vacancy(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=6000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(
        CurrentSession,
        on_delete=models.SET_NULL,
        to_field="session",
        null=True,
        blank=True,
    )
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=100, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "vacancies"
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f"{self.title} in {self.company}"


class Company(models.Model):
    company = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "companies"


class AdminVacancy(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=6000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(
        CurrentSession,
        on_delete=models.SET_NULL,
        to_field="session",
        null=True,
        blank=True,
    )
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "admin_last_session"
        verbose_name = "Admin vacancy"
        verbose_name_plural = "Admin vacancies"

    def __str__(self):
        return f"{self.title} in {self.company}"
