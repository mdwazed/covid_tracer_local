from django.db import models

# Create your models here.


class PersInfo(models.Model):
    user_gen_id = models.CharField(max_length=20)
    app_gen_id = models.IntegerField(unique=True)
    pers_num = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50,)
    rank = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)
    mobile_num = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.sta_name