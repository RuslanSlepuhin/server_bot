from django.db import models
from django.utils import timezone

class FormAnswerModel(models.Model):
    data = models.JSONField()
    email = models.CharField(max_length=100, null=True, blank=True)
    label = models.JSONField(blank=True, null=True)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)

class CustomFormModel(models.Model):
    form_name = models.CharField(max_length=100, blank=False, null=False)
    message = models.CharField(max_length=1000, blank=False, null=False)
    questions = models.JSONField(blank=False, null=False)

    def __str__(self):
        return self.form_name

