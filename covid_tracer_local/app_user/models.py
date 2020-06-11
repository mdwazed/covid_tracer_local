from django.db import models

# Create your models here.

class Unit(models.Model):
    unit_name = models.CharField(max_length=50)
    sta_name = models.CharField(max_length=50)

    def __str__(self):
        return self.unit_name

    def natural_key(self):
        return(self.unit_name)

class PersInfo(models.Model):
    user_gen_id = models.CharField(max_length=20)
    app_gen_id = models.IntegerField(unique=True)
    pers_num = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50,)
    rank = models.CharField(max_length=50, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    mobile_num = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.sta_name