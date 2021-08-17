# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Weathercache(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=36)  # Field name made lowercase.
    citytitle = models.CharField(db_column='CityTitle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    woeid = models.IntegerField(db_column='WoeID')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    maxtemp = models.SmallIntegerField(db_column='MaxTemp')  # Field name made lowercase.
    mintemp = models.SmallIntegerField(db_column='MinTemp')  # Field name made lowercase.
    humidity = models.SmallIntegerField(db_column='Humidity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WeatherCache'
        unique_together = (('woeid', 'date'),)