from django.db import models

# Create your models here.
class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100)

class Seenlist(models.Model):   
    id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    review = models.TextField(default='')
    rating = models.IntegerField(default=0)
    date_watched = models.DateField(default='1999-08-29')

    
    def __str__(self):
        return self.title