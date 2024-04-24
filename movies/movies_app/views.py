from django.shortcuts import render
from django.http import HttpRequest
import tmdbsimple as tmdb
from dotenv import load_dotenv
import os
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from movies_app.models import Watchlist, Seenlist

load_dotenv()
tmdb.API_KEY = os.getenv("API_KEY")
# Create your views here.
@csrf_exempt
def index(request: HttpRequest):
    if request.method == 'POST':
        if 'roll' in request.POST:
            movie = roll()
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
            if Watchlist.objects.filter(movie_id=id).exists():
                messages.error(request, f'"{ movie }" already exists in your watchlist!')
                return render(request, 'movies_app/index.html')
            if Seenlist.objects.filter(movie_id=id).exists():
                messages.error(request, f'"{ movie }" already exists in your seenlist!')
                return render(request, 'movies_app/index.html')
            movie = Watchlist(movie_id=id, title=movie, seen=False, review="None")
            movie.save()
            messages.success(request, f'"{ movie }" added to your watchlist!')
            return render(request, 'movies_app/index.html')

    return render(request, 'movies_app/index.html')

def roll():
    movie_to_watch = Watchlist.objects.order_by('?').first()
    print(movie_to_watch.title)
    movie_details = get_movie_info_by_id(movie_to_watch.movie_id)
    return movie_details

def get_movie_list(title: str):
    search = tmdb.Search()
    response = search.movie(query=title)
    return response['results'] if response['total_results'] > 0 else None

def get_movie_info_by_id(id: int):
    movie = tmdb.Movies(id)
    return movie.info() if movie else None