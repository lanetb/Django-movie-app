import csv
import os
import tmdbsimple as tmdb
from movies_app.models import Watchlist, Seenlist
from dotenv import load_dotenv

def run():
    load_dotenv()
    tmdb.API_KEY = os.getenv("API_KEY")
    with open('movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        Watchlist.objects.all().delete()
        Seenlist.objects.all().delete()
        tmdb.API_KEY = os.getenv('API_KEY')

        for row in reader:
            print(row)
            search = tmdb.Search()
            response = search.movie(query=row[0])
            movie = response['results'] if response['total_results'] > 0 else None

            if movie and not Watchlist.objects.filter(movie_id = movie[0]["id"]).exists() and not Seenlist.objects.filter(movie_id = movie[0]["id"]).exists():
                movie = movie[0]
                if row[1] == 'True':
                    movie = Seenlist(title=row[0], movie_id=movie['id'], overview=movie['overview'])
                    movie.save()
                else:
                    movie = Watchlist(title=row[0], movie_id=movie['id'], overview=movie['overview'], poster_url=f'https://image.tmdb.org/t/p/w500{movie['poster_path']}')
                    movie.save()