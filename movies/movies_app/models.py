from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    seen = models.BooleanField(default=False)
    review = models.TextField(blank=True, null=True, default=None)

    
    def __str__(self):
        return self.title