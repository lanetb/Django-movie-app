from movies_app.models import Movie
import csv

def run():
    with open('movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        Movie.objects.all().delete()

        for row in reader:
            print(row)
            movie = Movie(title=row[0], seen=row[1], review=row[2])
            movie.save()