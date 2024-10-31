from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from typing import List


class AdminCopy(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=100, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'admin_copy'


class AdminVacancy(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'admin_last_session'


class AdminTemporary(models.Model):
    id_admin_channel = models.CharField(max_length=20, blank=True, null=True)
    id_admin_last_session_table = models.CharField(max_length=20, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'admin_temporary'


class Analyst(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    analyst_unsorted = models.IntegerField(blank=True, null=True)
    analyst_all = models.IntegerField(blank=True, null=True)
    analyst_unique = models.IntegerField(blank=True, null=True)
    analyst_sys_analyst = models.IntegerField(blank=True, null=True)
    analyst_data_analyst = models.IntegerField(blank=True, null=True)
    analyst_ba = models.IntegerField(blank=True, null=True)
    analyst_data_scientist = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'analyst'


class Archive(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'archive'


class Ba(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)

    class Meta:
        db_table = 'ba'


class Backend(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey('CurrentSession', models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    backend_python = models.IntegerField(blank=True, null=True)
    backend_all = models.IntegerField(blank=True, null=True)
    backend_unique = models.IntegerField(blank=True, null=True)
    backend_java = models.IntegerField(blank=True, null=True)
    backend_nodejs = models.IntegerField(blank=True, null=True)
    backend_c = models.IntegerField(blank=True, null=True)
    backend_net = models.IntegerField(blank=True, null=True)
    backend_unsorted = models.IntegerField(blank=True, null=True)
    backend_data_engineer = models.IntegerField(blank=True, null=True)
    backend_php = models.IntegerField(blank=True, null=True)
    backend_laravel = models.IntegerField(blank=True, null=True)
    backend_ruby = models.IntegerField(blank=True, null=True)
    backend_golang = models.IntegerField(blank=True, null=True)
    backend_one_c = models.IntegerField(blank=True, null=True)
    backend_scala = models.IntegerField(blank=True, null=True)
    backend_ml = models.IntegerField(blank=True, null=True)
    backend_delphi = models.IntegerField(blank=True, null=True)
    backend_abap = models.IntegerField(blank=True, null=True)
    backend_unity = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'backend'


class Company(models.Model):
    company = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'companies'


class CountriesCities(models.Model):
    country = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'countries_cities'


class CurrentSession(models.Model):
    session = models.CharField(unique=True, max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'current_session'


class Designer(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    designer_unsorted = models.IntegerField(blank=True, null=True)
    designer_all = models.IntegerField(blank=True, null=True)
    designer_unique = models.IntegerField(blank=True, null=True)
    designer_ui_ux = models.IntegerField(blank=True, null=True)
    designer_game_designer = models.IntegerField(blank=True, null=True)
    designer_graphic = models.IntegerField(blank=True, null=True)
    designer_motion = models.IntegerField(blank=True, null=True)
    designer_ddd = models.IntegerField(blank=True, null=True)
    designer_dd = models.IntegerField(blank=True, null=True)
    designer_illustrator = models.IntegerField(blank=True, null=True)
    designer_uxre_searcher = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'designer'


class Devops(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    devops_unsorted = models.IntegerField(blank=True, null=True)
    devops_all = models.IntegerField(blank=True, null=True)
    devops_unique = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'devops'


class FollowersStatistics(models.Model):
    channel = models.CharField(max_length=150, blank=True, null=True)
    id_user = models.CharField(max_length=30, blank=True, null=True)
    access_hash = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    join_time = models.DateTimeField(blank=True, null=True)
    is_bot = models.BooleanField(blank=True, null=True)
    mutual_contact = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'followers_statistics'


class Frontend(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    frontend_react = models.IntegerField(blank=True, null=True)
    frontend_all = models.IntegerField(blank=True, null=True)
    frontend_unique = models.IntegerField(blank=True, null=True)
    frontend_unsorted = models.IntegerField(blank=True, null=True)
    frontend_angular = models.IntegerField(blank=True, null=True)
    frontend_vue = models.IntegerField(blank=True, null=True)
    frontend_bitrix = models.IntegerField(blank=True, null=True)
    frontend_django = models.IntegerField(blank=True, null=True)
    frontend_wordpress = models.IntegerField(blank=True, null=True)
    frontend_joomla = models.IntegerField(blank=True, null=True)
    frontend_drupal = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'frontend'


class Fullstack(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)

    class Meta:
        db_table = 'fullstack'


class Game(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    game_unsorted = models.IntegerField(blank=True, null=True)
    game_all = models.IntegerField(blank=True, null=True)
    game_unique = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'game'


class Hr(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    hr_unsorted = models.IntegerField(blank=True, null=True)
    hr_all = models.IntegerField(blank=True, null=True)
    hr_unique = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hr'


class Junior(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    junior_unsorted = models.IntegerField(blank=True, null=True)
    junior_all = models.IntegerField(blank=True, null=True)
    junior_unique = models.IntegerField(blank=True, null=True)
    junior_backend = models.IntegerField(blank=True, null=True)
    junior_devops = models.IntegerField(blank=True, null=True)
    junior_sales_manager = models.IntegerField(blank=True, null=True)
    junior_mobile = models.IntegerField(blank=True, null=True)
    junior_game = models.IntegerField(blank=True, null=True)
    junior_frontend = models.IntegerField(blank=True, null=True)
    junior_hr = models.IntegerField(blank=True, null=True)
    junior_designer = models.IntegerField(blank=True, null=True)
    junior_analyst = models.IntegerField(blank=True, null=True)
    junior_qa = models.IntegerField(blank=True, null=True)
    junior_pm = models.IntegerField(blank=True, null=True)
    junior_marketing = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'junior'


class LastAutopushingTime(models.Model):
    time = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'last_autopushing_time'


class Marketing(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    marketing_seo = models.IntegerField(blank=True, null=True)
    marketing_all = models.IntegerField(blank=True, null=True)
    marketing_unique = models.IntegerField(blank=True, null=True)
    marketing_unsorted = models.IntegerField(blank=True, null=True)
    marketing_smm = models.IntegerField(blank=True, null=True)
    marketing_content_manager = models.IntegerField(blank=True, null=True)
    marketing_link_builder = models.IntegerField(blank=True, null=True)
    marketing_context = models.IntegerField(blank=True, null=True)
    marketing_copyrighter = models.IntegerField(blank=True, null=True)
    marketing_media_buyer = models.IntegerField(blank=True, null=True)
    marketing_tech_writer = models.IntegerField(blank=True, null=True)
    marketing_email_marketer = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'marketing'


class Middle(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)

    class Meta:
        db_table = 'middle'


class Mobile(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    mobile_unsorted = models.IntegerField(blank=True, null=True)
    mobile_all = models.IntegerField(blank=True, null=True)
    mobile_unique = models.IntegerField(blank=True, null=True)
    mobile_android = models.IntegerField(blank=True, null=True)
    mobile_cross_mobile = models.IntegerField(blank=True, null=True)
    mobile_react_native = models.IntegerField(blank=True, null=True)
    mobile_ios = models.IntegerField(blank=True, null=True)
    mobile_flutter = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'mobile'


class NoSort(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)

    class Meta:
        db_table = 'no_sort'


class ParserAtWork(models.Model):
    parser_at_work = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'parser_at_work'


class Pm(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    pm_project = models.IntegerField(blank=True, null=True)
    pm_all = models.IntegerField(blank=True, null=True)
    pm_unique = models.IntegerField(blank=True, null=True)
    pm_unsorted = models.IntegerField(blank=True, null=True)
    pm_product = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'pm'


class Product(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    product_unsorted = models.IntegerField(blank=True, null=True)
    product_all = models.IntegerField(blank=True, null=True)
    product_unique = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'product'


class Qa(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    qa_aqa = models.IntegerField(blank=True, null=True)
    qa_all = models.IntegerField(blank=True, null=True)
    qa_unique = models.IntegerField(blank=True, null=True)
    qa_unsorted = models.IntegerField(blank=True, null=True)
    qa_manual_qa = models.IntegerField(blank=True, null=True)
    qa_support = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'qa'


class Reject(models.Model):
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
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
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
        db_table = 'reject'


class SalesManager(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=30, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    sales_manager_unsorted = models.IntegerField(blank=True, null=True)
    sales_manager_all = models.IntegerField(blank=True, null=True)
    sales_manager_unique = models.IntegerField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'sales_manager'


class Senior(models.Model):
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
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.ForeignKey(CurrentSession, models.DO_NOTHING, db_column='session', to_field='session', blank=True, null=True)

    class Meta:
        db_table = 'senior'


class ShortsAtWork(models.Model):
    shorts_at_work = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'shorts_at_work'


class ShortsSessionName(models.Model):
    session_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'shorts_session_name'


class StatsDb(models.Model):
    created_at = models.DateField(blank=True, null=True)
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    designer_all = models.IntegerField(blank=True, null=True)
    designer_unique = models.IntegerField(blank=True, null=True)
    game_all = models.IntegerField(blank=True, null=True)
    game_unique = models.IntegerField(blank=True, null=True)
    product_all = models.IntegerField(blank=True, null=True)
    product_unique = models.IntegerField(blank=True, null=True)
    mobile_all = models.IntegerField(blank=True, null=True)
    mobile_unique = models.IntegerField(blank=True, null=True)
    pm_all = models.IntegerField(blank=True, null=True)
    pm_unique = models.IntegerField(blank=True, null=True)
    sales_manager_all = models.IntegerField(blank=True, null=True)
    sales_manager_unique = models.IntegerField(blank=True, null=True)
    analyst_all = models.IntegerField(blank=True, null=True)
    analyst_unique = models.IntegerField(blank=True, null=True)
    frontend_all = models.IntegerField(blank=True, null=True)
    frontend_unique = models.IntegerField(blank=True, null=True)
    marketing_all = models.IntegerField(blank=True, null=True)
    marketing_unique = models.IntegerField(blank=True, null=True)
    devops_all = models.IntegerField(blank=True, null=True)
    devops_unique = models.IntegerField(blank=True, null=True)
    hr_all = models.IntegerField(blank=True, null=True)
    hr_unique = models.IntegerField(blank=True, null=True)
    backend_all = models.IntegerField(blank=True, null=True)
    backend_unique = models.IntegerField(blank=True, null=True)
    qa_all = models.IntegerField(blank=True, null=True)
    qa_unique = models.IntegerField(blank=True, null=True)
    junior_all = models.IntegerField(blank=True, null=True)
    junior_unique = models.IntegerField(blank=True, null=True)
    junior_hr = models.IntegerField(blank=True, null=True)
    junior_marketing = models.IntegerField(blank=True, null=True)
    junior_analyst = models.IntegerField(blank=True, null=True)
    junior_backend = models.IntegerField(blank=True, null=True)
    junior_unsorted = models.IntegerField(blank=True, null=True)
    junior_pm = models.IntegerField(blank=True, null=True)
    junior_devops = models.IntegerField(blank=True, null=True)
    junior_sales_manager = models.IntegerField(blank=True, null=True)
    junior_frontend = models.IntegerField(blank=True, null=True)
    junior_designer = models.IntegerField(blank=True, null=True)
    junior_qa = models.IntegerField(blank=True, null=True)
    junior_mobile = models.IntegerField(blank=True, null=True)
    junior_game = models.IntegerField(blank=True, null=True)
    pm_project = models.IntegerField(blank=True, null=True)
    pm_product = models.IntegerField(blank=True, null=True)
    pm_unsorted = models.IntegerField(blank=True, null=True)
    qa_unsorted = models.IntegerField(blank=True, null=True)
    qa_manual_qa = models.IntegerField(blank=True, null=True)
    qa_aqa = models.IntegerField(blank=True, null=True)
    qa_support = models.IntegerField(blank=True, null=True)
    devops_unsorted = models.IntegerField(blank=True, null=True)
    mobile_ios = models.IntegerField(blank=True, null=True)
    mobile_android = models.IntegerField(blank=True, null=True)
    mobile_cross_mobile = models.IntegerField(blank=True, null=True)
    mobile_unsorted = models.IntegerField(blank=True, null=True)
    game_unsorted = models.IntegerField(blank=True, null=True)
    frontend_react = models.IntegerField(blank=True, null=True)
    frontend_vue = models.IntegerField(blank=True, null=True)
    frontend_bitrix = models.IntegerField(blank=True, null=True)
    frontend_unsorted = models.IntegerField(blank=True, null=True)
    frontend_angular = models.IntegerField(blank=True, null=True)
    frontend_wordpress = models.IntegerField(blank=True, null=True)
    frontend_django = models.IntegerField(blank=True, null=True)
    backend_php = models.IntegerField(blank=True, null=True)
    backend_python = models.IntegerField(blank=True, null=True)
    backend_java = models.IntegerField(blank=True, null=True)
    backend_golang = models.IntegerField(blank=True, null=True)
    backend_unsorted = models.IntegerField(blank=True, null=True)
    backend_c = models.IntegerField(blank=True, null=True)
    backend_nodejs = models.IntegerField(blank=True, null=True)
    backend_unity = models.IntegerField(blank=True, null=True)
    backend_data_engineer = models.IntegerField(blank=True, null=True)
    backend_one_c = models.IntegerField(blank=True, null=True)
    backend_net = models.IntegerField(blank=True, null=True)
    backend_ruby = models.IntegerField(blank=True, null=True)
    backend_delphi = models.IntegerField(blank=True, null=True)
    marketing_unsorted = models.IntegerField(blank=True, null=True)
    marketing_context = models.IntegerField(blank=True, null=True)
    marketing_smm = models.IntegerField(blank=True, null=True)
    marketing_tech_writer = models.IntegerField(blank=True, null=True)
    marketing_media_buyer = models.IntegerField(blank=True, null=True)
    marketing_seo = models.IntegerField(blank=True, null=True)
    marketing_copyrighter = models.IntegerField(blank=True, null=True)
    marketing_link_builder = models.IntegerField(blank=True, null=True)
    marketing_content_manager = models.IntegerField(blank=True, null=True)
    backend_abap = models.IntegerField(blank=True, null=True)
    designer_ui_ux = models.IntegerField(blank=True, null=True)
    designer_motion = models.IntegerField(blank=True, null=True)
    designer_graphic = models.IntegerField(blank=True, null=True)
    designer_unsorted = models.IntegerField(blank=True, null=True)
    designer_ddd = models.IntegerField(blank=True, null=True)
    designer_illustrator = models.IntegerField(blank=True, null=True)
    designer_game_designer = models.IntegerField(blank=True, null=True)
    designer_dd = models.IntegerField(blank=True, null=True)
    sales_manager_unsorted = models.IntegerField(blank=True, null=True)
    analyst_unsorted = models.IntegerField(blank=True, null=True)
    analyst_data_analyst = models.IntegerField(blank=True, null=True)
    analyst_ba = models.IntegerField(blank=True, null=True)
    analyst_sys_analyst = models.IntegerField(blank=True, null=True)
    analyst_data_scientist = models.IntegerField(blank=True, null=True)
    frontend_drupal = models.IntegerField(blank=True, null=True)
    marketing_email_marketer = models.IntegerField(blank=True, null=True)
    backend_scala = models.IntegerField(blank=True, null=True)
    frontend_joomla = models.IntegerField(blank=True, null=True)
    hr_unsorted = models.IntegerField(blank=True, null=True)
    marketing_copywriter = models.IntegerField(blank=True, null=True)
    marketing_influencer = models.IntegerField(blank=True, null=True)
    marketing_marketplace = models.IntegerField(blank=True, null=True)
    designer_uxre_searcher = models.IntegerField(blank=True, null=True)
    marketing_aso = models.IntegerField(blank=True, null=True)
    mobile_flutter = models.IntegerField(blank=True, null=True)
    backend_embedded = models.IntegerField(blank=True, null=True)
    mobile_react_native = models.IntegerField(blank=True, null=True)
    backend_ml = models.IntegerField(blank=True, null=True)
    backend_laravel = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'stats_db'


class UserRequests(models.Model):
    user_id = models.BigIntegerField(blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=500, blank=True, null=True)
    level = models.CharField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    work_format = models.CharField(max_length=500, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    selected_notification = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='последнее обновление', blank=True, null=True)

    class Meta:
        db_table = 'user_requests'


class Users(models.Model):
    id_user = models.CharField(max_length=20, blank=True, null=True)
    api_id = models.CharField(max_length=20, blank=True, null=True)
    api_hash = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'users'


class Vacancies(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.CharField(max_length=15, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'vacancies'


class VacancyStock(models.Model):
    chat_name = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    body = models.CharField(max_length=10000, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    vacancy = models.CharField(max_length=700, blank=True, null=True)
    vacancy_url = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    english = models.CharField(max_length=100, blank=True, null=True)
    relocation = models.CharField(max_length=100, blank=True, null=True)
    job_type = models.CharField(max_length=700, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    salary = models.CharField(max_length=300, blank=True, null=True)
    experience = models.CharField(max_length=700, blank=True, null=True)
    contacts = models.CharField(max_length=500, blank=True, null=True)
    time_of_public = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    agregator_link = models.CharField(max_length=200, blank=True, null=True)
    session = models.CharField(max_length=15, blank=True, null=True)
    sended_to_agregator = models.CharField(max_length=30, blank=True, null=True)
    sub = models.CharField(max_length=250, blank=True, null=True)
    tags = models.CharField(max_length=700, blank=True, null=True)
    full_tags = models.CharField(max_length=700, blank=True, null=True)
    full_anti_tags = models.CharField(max_length=700, blank=True, null=True)
    short_session_numbers = models.CharField(max_length=300, blank=True, null=True)
    level = models.CharField(max_length=70, blank=True, null=True)
    approved = models.CharField(max_length=150, blank=True, null=True)
    closed = models.BooleanField(blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(max_length=20, blank=True, null=True)
    salary_period = models.CharField(max_length=50, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    salary_from_usd_month = models.IntegerField(blank=True, null=True)
    salary_to_usd_month = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'vacancy_stock'


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
    class JobFormat(models.TextChoices):
        REMOTE = "удалённая"
        OFFICE = "офис"
        HYBRID = "гибкий график"

    class Directions(models.TextChoices):
        DEVELOPING = "developing"
        ANALYTICS = "analytics"
        SUPPORT = "support"
        RECRUITING = "recruiting"
        TESTING = "testing"
        DESIGN = "design"
        MANAGEMENT = "management"
        SECURITY = "security"
        CONTENT = "content"
        MARKETING = "marketing"

    class Qualification(models.TextChoices):
        TRAINEE = "trainee"
        JUNIOR = "junior"
        MIDDLE = "middle"
        SENIOR = "senior"
        LEAD = "lead"
        DIRECTOR = "director"

    class Role(models.TextChoices):
        APPLICANT = "соискатель"
        EMPLOYER = "работодатель"
        MENTOR = "ментор"

    class SalaryPeriod(models.TextChoices):
        HOUR = "час"
        DAY = "день"
        MONTH = "месяц"
        YEAR = "год"

    class Currencies(models.TextChoices):
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"
        BYN = "BYN"
        KZT = "KZT"
        PLN = "PLN"
        UAH = "UAH"

    class Gender(models.TextChoices):
        MALE = "мужской"
        FEMALE = "женский"
        OTHER = "другой"

    email = models.EmailField(unique=True, blank=False, null=False)
    surname = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(
        max_length=16, blank=True, null=True, choices=Gender.choices
    )
    birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    citizen = models.CharField(max_length=32, blank=True, null=True)
    education = models.JSONField(blank=True, null=True)
    experience = models.JSONField(blank=True, null=True)
    networks = models.JSONField(blank=True, null=True)
    languages = models.JSONField(blank=True, null=True)
    relocation = models.BooleanField(blank=True, null=True)
    relocation_prefer = models.CharField(max_length=32, blank=True, null=True)
    phonenumber = models.CharField(max_length=32, blank=True, null=True)
    cv = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    currency = models.CharField(
        max_length=4, blank=True, null=True, choices=Currencies.choices
    )
    period = models.CharField(
        max_length=16, blank=True, null=True, choices=SalaryPeriod.choices
    )
    taxes = models.BooleanField(blank=True, null=True)
    jobtitle = models.CharField(max_length=64, blank=True, null=True)
    jobformat = ArrayField(models.CharField(max_length=32), blank=True, null=True)
    jobtype = ArrayField(models.CharField(max_length=32), blank=True, null=True)
    hardskills = ArrayField(models.CharField(max_length=256), blank=True, null=True)
    softskills = ArrayField(models.CharField(max_length=256), blank=True, null=True)
    volunteer = models.CharField(max_length=2048, blank=True, null=True)
    visibility = models.BooleanField(blank=True, null=True)
    hidefor = ArrayField(models.CharField(max_length=128), blank=True, null=True)
    role = models.CharField(max_length=32, blank=True, null=True, choices=Role.choices)
    qualification = ArrayField(
        models.CharField(max_length=128, choices=Qualification.choices),
        blank=True,
        null=True,
    )
    photo = models.ImageField(blank=True, null=True)
    banner = models.ImageField(blank=True, null=True)
    about = models.CharField(max_length=2048, blank=True, null=True)
    viewed = ArrayField(models.IntegerField(), blank=True, null=True)
    favorites = ArrayField(models.IntegerField(), blank=True, null=True)
    responded = models.JSONField(blank=True, null=True)
    directvision = models.BooleanField(blank=True, null=True)
    subscriber = ArrayField(models.IntegerField(), blank=True, null=True)
    telegram_id = models.IntegerField(blank=True, null=True)
    profession = models.CharField(
        choices=Directions.choices, blank=True, null=True, max_length=20
    )
    specialization = models.CharField(max_length=32, blank=True, null=True)
    sub = models.CharField(max_length=32, blank=True, null=True)
    pr_languages = ArrayField(models.CharField(max_length=64), blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=256), blank=True, null=True)
    tools = ArrayField(models.CharField(max_length=256), blank=True, null=True)
    job_format = models.CharField(
        max_length=32, blank=True, null=True, choices=JobFormat.choices
    )
    tg1_subscriber = models.BooleanField(blank=True, null=True)
    tg2_subscriber = models.BooleanField(blank=True, null=True)
    tgbot_user = models.BooleanField(blank=True, null=True)
    company_id = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.SET_NULL
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Source(models.Model):
    class Types(models.TextChoices):
        TGCHANNEL = "tgchannel"
        SITE = "site"
        TGBOT = "tgbot"

    name = models.CharField(max_length=150, blank=True, null=True)
    tgchannel_id = models.IntegerField(blank=True, null=True)
    url = models.EmailField(max_length=150, blank=True, null=True)
    sourcetype = models.CharField(
        blank=True, null=True, choices=Types.choices, max_length=15
    )
    istarget = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = "sources"
        verbose_name = "Source"
        verbose_name_plural = "Sources"


class Currency(models.Model):
    class Currencies(models.TextChoices):
        USD = "USD"
        EUR = "EUR"
        RUB = "RUB"
        BYN = "BYN"
        KZT = "KZT"
        PLN = "PLN"
        UAH = "UAH"

    currency = models.CharField(choices=Currencies.choices, max_length=4)
    rate_usd = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)


class Vacancy(models.Model):
    class Directions(models.TextChoices):
        DEVELOPING = "developing"
        ANALYTICS = "analytics"
        SUPPORT = "support"
        RECRUITING = "recruiting"
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

    source_id = models.ForeignKey(
        Source, blank=True, null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=512, blank=True, null=True)
    body = models.CharField(max_length=10240, blank=True, null=True)
    profession = models.CharField(
        choices=Directions.choices, blank=True, null=True, max_length=20
    )
    vacancy = models.CharField(max_length=512, blank=True, null=True)
    vacancy_url = models.URLField(max_length=128, blank=True, null=True)
    company = models.CharField(max_length=128, blank=True, null=True)
    company_id = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True
    )
    english = models.CharField(max_length=16, blank=True, null=True)
    job_type = models.CharField(
        choices=JobType.choices, blank=True, null=True, max_length=20
    )
    country = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    salary = models.CharField(max_length=64, blank=True, null=True)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_currency = models.CharField(
        choices=Currencies.choices, blank=True, null=True, max_length=4
    )
    currency_id = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, blank=True, null=True
    )
    salary_period = models.CharField(
        choices=SalaryPeriod.choices, blank=True, null=True, max_length=10
    )
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
    responded = ArrayField(models.IntegerField(), blank=True, null=True)

    class Meta:
        db_table = "full_vacancies"
        verbose_name = "full_Vacancy"
        verbose_name_plural = "full_Vacancies"

    def __str__(self):
        return f"{self.title} in {self.company}"


class Quizz(models.Model):
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    questions = models.JSONField(blank=True, null=True)


class Follower(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    stat_date = models.DateField(blank=True, null=True)
    followers_total = models.IntegerField(blank=True, null=True)


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    added = models.BooleanField(blank=True, null=True)


class Filter(models.Model):
    vacancy = models.ForeignKey(
        Vacancy, on_delete=models.SET_NULL, blank=True, null=True
    )
    approved_admin = models.BooleanField(blank=True, null=True)
    approved_gemini = models.JSONField(blank=True, null=True)
    approved_filter = models.BooleanField(blank=True, null=True)
    sent_to_agregator = models.IntegerField(blank=True, null=True)
    full_tags = models.CharField(max_length=200, blank=True, null=True)
    full_antitags = models.CharField(max_length=200, blank=True, null=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True
    )
    review_date = models.DateTimeField(auto_now_add=True)
    review_text = models.CharField(max_length=1024, blank=True, null=True)


class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    companies_id = ArrayField(models.IntegerField(), blank=True, null=True)
    vacancies_id = ArrayField(models.IntegerField(), blank=True, null=True)
