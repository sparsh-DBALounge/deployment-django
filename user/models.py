from django.db import models
from utils.models import TimeStampModel

class User(TimeStampModel):
    name = models.CharField(max_length=15)
    email = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name