from django.shortcuts import render
from django.http import HttpRequest
import tmdbsimple as tmdb
from movies_app.models import Movie
from dotenv import load_dotenv
import os
from django.contrib import messages

load_dotenv()
tmdb.API_KEY = os.getenv("API_KEY")
# Create your views here.
def index(request: HttpRequest):
    if request.method == 'POST':
        if 'roll' in request.POST:
            movie_title = Movie.objects.order_by('?').first()
            print(movie_title.title)
            print(movie_title.seen)
            if movie_title.seen:
                index(request)
            if movie_title.movie_id == 0:
                movie = get_movie_info_title(movie_title.title)
                movie_title.movie_id = movie['id']
                movie_title.save()
            else:
                movie = get_movie_info_idd(movie_title.movie_id)
            context = {
                'movie': movie,
                'year': movie['release_date'][:4],
            }
            return render(request, 'movies_app/movie.html', context)
        elif 'add' in request.POST:
            return render(request, 'movies_app/add.html')
        elif 'search' in request.POST:
            print(request.POST['search'])
            movies = get_movie_list(request.POST['title'])
            context = {
                'movies': movies,
            }
            return render(request, 'movies_app/search.html', context)
        elif 'add_movie_to_database' in request.POST:
            
            movie = request.POST['title']
            id = request.POST['movie_id']
            if Movie.objects.filter(movie_id=id).exists():
                messages.error(request, f'"{ movie }" already exists in your watchlist!')
                return render(request, 'movies_app/index.html')
            if Movie.objects.filter(title=movie).exists():
                messages.error(request, f'"{ movie }" already exists in your watchlist!')
                return render(request, 'movies_app/index.html')
            movie = Movie(movie_id=id, title=movie, seen=False, review="")
            movie.save()
            messages.success(request, f'"{ movie }" added to your watchlist!')
            return render(request, 'movies_app/index.html')

    return render(request, 'movies_app/index.html')

def get_movie_list(title: str):
    search = tmdb.Search()
    response = search.movie(query=title)
    return response['results'] if response['total_results'] > 0 else None

def get_movie_info(title: str):
    search = tmdb.Search()
    response = search.movie(query=title)
    return response['results'][0] if response['total_results'] > 0 else None

def get_movie_info_title(title: str):
    movie = get_movie_info(title)
    movie = tmdb.Movies(movie['id'])
    return movie.info() if movie else None

def get_movie_info_idd(id: int):
    movie = tmdb.Movies(id)
    return movie.info() if movie else None