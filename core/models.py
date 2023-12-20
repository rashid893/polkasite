from django.db import models
from datetime import datetime




class Delegate(models.Model):
    key = models.CharField(max_length=1000, unique=True)
    name = models.CharField(max_length=1000)
    url = models.URLField()
    description = models.TextField()
    signature = models.TextField()
    hot_key = models.CharField(max_length=1000)
    nominators = models.PositiveIntegerField(null=True, blank=True)
    total_stake = models.FloatField(null=True, blank=True)
    apr_average = models.FloatField(null=True, blank=True)
    apr = models.FloatField(null=True, blank=True)

    emission=models.CharField(max_length=100,null=True, blank=True)
    reward=models.CharField(max_length=100,null=True, blank=True)
    benefits = models.FloatField(null=True, blank=True)
    tooltips = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Supply(models.Model):
    volume_24h = models.FloatField(default=0.0)
    current_price = models.FloatField(default=0.0)
    change_24h = models.FloatField(default=0.0)
    circulating_supply = models.FloatField(default=0.0)
    total_stakes = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)
    total_supply = models.FloatField(default=0.0)
    percent_staked =  models.FloatField(default=0.0)

class DelegateUndelegateStatus(models.Model):
    wallet_address = models.CharField(max_length=255)
    amount = models.CharField(max_length=30)
    action = models.CharField(max_length=50)
    validator = models.CharField(max_length=255)
    date = models.DateTimeField()

class AprSave(models.Model):
    validator=models.CharField(max_length=50)
    apr = models.FloatField(null=True, blank=True)
    key = models.CharField(max_length=1000)
    date = models.DateTimeField()


class WeeklyAprAverage(models.Model):
    validator=models.CharField(max_length=50)
    average_apr = models.FloatField(null=True, blank=True)
    key = models.CharField(max_length=1000)
    date = models.DateTimeField()