# Generated by Django 4.1.4 on 2024-04-05 12:55

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_currency_source_alter_adminvacancy_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AddField(
            model_name="user",
            name="about",
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="banner",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="user",
            name="birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="citizen",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="company_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.company",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.CharField(
                blank=True,
                choices=[
                    ("USD", "Usd"),
                    ("EUR", "Eur"),
                    ("RUB", "Rub"),
                    ("BYN", "Byn"),
                    ("KZT", "Kzt"),
                    ("PLN", "Pln"),
                    ("UAH", "Uah"),
                ],
                max_length=4,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="cv",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="directvision",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="education",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="experience",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="favorites",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, null=True, size=None
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("мужской", "Male"),
                    ("женский", "Female"),
                    ("другой", "Other"),
                ],
                max_length=16,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="hardskills",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="hidefor",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=128),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="job_format",
            field=models.CharField(
                blank=True,
                choices=[
                    ("удалённая", "Remote"),
                    ("офис", "Office"),
                    ("гибкий график", "Hybrid"),
                ],
                max_length=32,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="jobformat",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=32),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="jobtitle",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="jobtype",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=32),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="languages",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="networks",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="period",
            field=models.CharField(
                blank=True,
                choices=[
                    ("час", "Hour"),
                    ("день", "Day"),
                    ("месяц", "Month"),
                    ("год", "Year"),
                ],
                max_length=16,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phonenumber",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="user",
            name="portfolio",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="pr_languages",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=64),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profession",
            field=models.CharField(
                blank=True,
                choices=[
                    ("developing", "Developing"),
                    ("analytics", "Analytics"),
                    ("support", "Support"),
                    ("recruiting", "Recruiting"),
                    ("testing", "Testing"),
                    ("design", "Design"),
                    ("management", "Management"),
                    ("security", "Security"),
                    ("content", "Content"),
                    ("marketing", "Marketing"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="qualification",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("trainee", "Trainee"),
                        ("junior", "Junior"),
                        ("middle", "Middle"),
                        ("senior", "Senior"),
                        ("lead", "Lead"),
                        ("director", "Director"),
                    ],
                    max_length=128,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="relocation",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="relocation_prefer",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="responded",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("соискатель", "Applicant"),
                    ("работодатель", "Employer"),
                    ("ментор", "Mentor"),
                ],
                max_length=32,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="salary",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="skills",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="softskills",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="specialization",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="sub",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="subscriber",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, null=True, size=None
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="surname",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="taxes",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="telegram_id",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="tg1_subscriber",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="tg2_subscriber",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="tgbot_user",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="tools",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=256),
                blank=True,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="viewed",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, null=True, size=None
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="visibility",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="volunteer",
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="profession",
            field=models.CharField(
                blank=True,
                choices=[
                    ("developing", "Developing"),
                    ("analytics", "Analytics"),
                    ("support", "Support"),
                    ("recruiting", "Recruiting"),
                    ("testing", "Testing"),
                    ("design", "Design"),
                    ("management", "Management"),
                    ("security", "Security"),
                    ("content", "Content"),
                    ("marketing", "Marketing"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
