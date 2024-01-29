from django.db import models

class webFormModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    instrumentWorks = models.CharField(max_length=50, null=False, blank=False)
    whatAmount = models.CharField(max_length=50, null=False, blank=False)
    whatTradingStrategy = models.CharField(max_length=150, null=False, blank=False)
    optimalInvestmentPeriod = models.JSONField(null=False, blank=False)
    howToReach = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return str(self.name)
