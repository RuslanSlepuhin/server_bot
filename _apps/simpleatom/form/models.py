from django.db import models

class FormAnswerModel(models.Model):
    data = models.JSONField(blank=True, null=True)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return str(self.email)

class CustomFormModel(models.Model):
    form_name = models.CharField(max_length=100, blank=False, null=False)
    questions = models.JSONField(blank=False, null=False)

    # def __str__(self):
    #     return self.form_name

