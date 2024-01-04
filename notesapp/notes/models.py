from django.db import models
from users.models import Users

class Notes(models.Model):
    title = models.CharField(max_length=100, blank= False)
    description = models.TextField(blank=True)
    users = models.ForeignKey(Users, on_delete= models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
