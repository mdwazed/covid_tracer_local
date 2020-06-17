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
    user_gen_id = models.CharField(max_length=10)
    app_gen_id = models.CharField(max_length=10, unique=True)
    pers_num = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50,)
    rank = models.CharField(max_length=10, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    mobile_num = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        unique_together = ['user_gen_id', 'app_gen_id']
    def __str__(self):
        return self.name