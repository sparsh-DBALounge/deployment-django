from django.db import models
from user.models import User
from utils.models import TimeStampModel

class PriorityChoices(models.IntegerChoices):
    LOW = 1,      'Low'
    MEDIUM = 2,   'Medium'
    HIGH = 3,     'High'

class Todo(TimeStampModel):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    priority = models.IntegerField(choices=PriorityChoices.choices, default=PriorityChoices.LOW)
    deadline = models.DateField(blank=True, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='todos'
    )

    class Meta:
        db_table = 'todos'

    def __str__(self):
        return self.title
    