from django.db import models
from datetime import datetime
from django.utils import timezone
from accounts.models import CustomUser
# Create your models here.
#DataFlair Models
class PatientRecord(models.Model):
    user= models.ForeignKey(CustomUser,  on_delete=models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length = 50, blank=False)
    image = models.ImageField()
    desc = models.TextField(max_length = 100, default='No Description')
    Phone = models.PositiveIntegerField()
    Age = models.PositiveIntegerField()
    Date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name

