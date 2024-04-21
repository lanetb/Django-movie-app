from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    seen = models.BooleanField(default=False)
    review = models.TextField(blank=True, null=True, default=None)

    
    def __str__(self):
        return self.title