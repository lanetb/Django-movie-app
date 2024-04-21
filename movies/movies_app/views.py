from django.shortcuts import render
from django.http import HttpRequest
import tmdbsimple as tmdb
from movies_app.models import Movie

# Create your views here.
def index(request: HttpRequest):
    if request.method == 'POST':
        if 'roll' in request.POST:
            movie_title = Movie.objects.order_by('?').first()
            print(movie_title.title)
            print(movie_title.seen)
            if movie_title.seen:
                index(request)
            movie = get_movie_info_id(movie_title.title)
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
    return movie.info() if movie else None