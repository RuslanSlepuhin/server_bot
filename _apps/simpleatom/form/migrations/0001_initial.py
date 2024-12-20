# Generated by Django 4.2.11 on 2024-04-06 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=1000)),
                ('questions', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='FormAnswerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('label', models.JSONField(blank=True, null=True)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
