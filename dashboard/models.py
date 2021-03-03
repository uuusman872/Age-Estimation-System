from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
#DataFlair Models
class patient(models.Model):
    name = models.CharField(max_length = 50, blank=False)
    image = models.ImageField()
    desc = models.TextField(max_length = 100, default='No Description')
    Phone = models.PositiveIntegerField()
    Age = models.PositiveIntegerField()
    Date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

