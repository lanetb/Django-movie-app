from django.shortcuts import render
from django.http import HttpRequest
import tmdbsimple as tmdb
from movies_app.models import Movie

# Create your views here.
def index(request: HttpRequest):
    if request.method == 'POST':
        movie_title = Movie.objects.order_by('?').first().title
        print(movie_title)
        movie = get_movie_info_id(movie_title)
        context = {
            'movie': movie
        }
        return render(request, 'movies_app/movie.html', context)

    return render(request, 'movies_app/index.html')

tmdb.API_KEY = "20a8735681dba8eec22c80c76415287e"

def get_movie_info(title: str):
    search = tmdb.Search()
    response = search.movie(query=title)
    return response['results'][0] if response['total_results'] > 0 else None

def get_movie_info_id(title: str):
    movie = get_movie_info(title)
    movie = tmdb.Movies(movie['id'])
    print(movie.info())
    return movie.info() if movie else None