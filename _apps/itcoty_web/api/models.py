from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField


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


class Source(models.Model):
    class Types(models.TextChoices):
        TGCHANNEL = "tgchannel"
        SITE = "site"
        TGBOT = "tgbot"

    name = models.CharField(blank=True, null=True)
    tgchannel_id = models.IntegerField(blank=True, null=True)
    url = models.EmailField(max_length=150, blank=True, null=True)
    sourcetype = models.CharField(blank=True, null=True, choices=Types.choices)
    istarget = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "sources"
        verbose_name = "Source"
        verbose_name_plural = "Sources"


class Company(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    contacts = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(max_length=160, blank=True, null=True)
    website = models.URLField(max_length=160, blank=True, null=True)
    logo = models.ImageField(blank=True, null=True)
    voted_users = ArrayField(models.IntegerField(), blank=True, null=True)
    reviewed_users = ArrayField(models.IntegerField(), blank=True, null=True)
    mark = models.IntegerField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "companies"
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Currency(models.Model):
    class Currencies(models.TextChoices):
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"
        BYN = "BYN"
        KZT = "KZT"
        PLN = "PLN"
        UAH = "UAH"

    currency = models.CharField(choices=Currencies.choices)
    rate_usd = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)


class Vacancy(models.Model):
    class Directions(models.TextChoices):
        DEVELOPING = "developing"
        ANALYTICS = "analytics"
        SUPPORT = "support"
        RECRUTING = "recruting"
        TESTING = "testing"
        DESIGN = "design"
        MANAGEMENT = "management"
        SECURITY = "security"
        CONTENT = "content"
        MARKETING = "marketing"

    class JobType(models.TextChoices):
        ONETIME = "разовая"
        FULL = "полный день"
        SHORTTIME = "сокращенный день"
        FREETIME = "в свободное время"
        PARTTIME = "подработка"

    class Currencies(models.TextChoices):
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"
        BYN = "BYN"
        KZT = "KZT"
        PLN = "PLN"
        UAH = "UAH"

    class SalaryPeriod(models.TextChoices):
        MONTH = "month"
        YEAR = "year"
        JOB = "job"
        PROJECT = "project"
        UNIT = "unit"
        HOUR = "hour"
        DAY = "day"
        WEEK = "week"

    source_id = models.ForeignKey(Source, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=512, blank=True, null=True)
    body = models.CharField(max_length=10240, blank=True, null=True)
    profession = models.CharField(choices=Directions.choices, blank=True, null=True)
    vacancy = models.CharField(max_length=512, blank=True, null=True)
    vacancy_url = models.URLField(max_length=128, blank=True, null=True)
    company = models.CharField(max_length=128, blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    english = models.CharField(max_length=16, blank=True, null=True)
    job_type = models.CharField(choices=JobType.choices, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    salary = models.CharField(max_length=64, blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(choices=Currencies.choices, blank=True, null=True)
    currency_id = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)
    salary_period = models.CharField(choices=SalaryPeriod.choices, blank=True, null=True)
    experience = models.CharField(max_length=32, blank=True, null=True)
    contacts = models.CharField(max_length=64, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    sub = models.CharField(max_length=128, blank=True, null=True)
    tags = models.CharField(max_length=256, blank=True, null=True)
    full_tags = models.CharField(max_length=200, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=32, blank=True, null=True)
    approved_admin = models.BooleanField(blank=True, null=True)
    approved_gemini = models.BooleanField(blank=True, null=True)
    approved_filter = models.BooleanField(blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    specialization = models.CharField(max_length=32, blank=True, null=True)
    languages = models.CharField(max_length=64, blank=True, null=True)
    skills = models.CharField(max_length=256, blank=True, null=True)
    tools = models.CharField(max_length=256, blank=True, null=True)
    remote = models.BooleanField(blank=True, null=True)
    office = models.BooleanField(blank=True, null=True)
    relocation = models.BooleanField(blank=True, null=True)
    sent_to_aggregator = models.IntegerField(blank=True, null=True)
    trainee = models.BooleanField(blank=True, null=True)
    junior = models.BooleanField(blank=True, null=True)
    middle = models.BooleanField(blank=True, null=True)
    senior = models.BooleanField(blank=True, null=True)
    lead = models.BooleanField(blank=True, null=True)
    director = models.BooleanField(blank=True, null=True)
    internship = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "vacancies"
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return f"{self.title} in {self.company}"


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
