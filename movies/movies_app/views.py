from django.shortcuts import render
from django.http import HttpRequest
import tmdbsimple as tmdb
from dotenv import load_dotenv
import os
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from movies_app.models import Watchlist, Seenlist
from datetime import date

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
            movies = get_movie_list(request.POST['title'])

            context = {
                'movies': movies,
            }
            return render(request, 'movies_app/search.html', context)

        elif 'add_movie_to_database' in request.POST:
            movie = request.POST['title']
            movie_id = request.POST['movie_id']
            overview = request.POST['overview']
            poster_url = f'https://image.tmdb.org/t/p/w500{request.POST['poster_url']}'
            if Watchlist.objects.filter(movie_id=movie_id).exists():
                messages.error(
                    request, f'"{movie}" already exists in your watchlist!')
                return render(request, 'movies_app/index.html')
            if Seenlist.objects.filter(movie_id=movie_id).exists():
                messages.error(
                    request, f'"{movie}" already exists in your seenlist!')
                return render(request, 'movies_app/index.html')
            movie = Watchlist(movie_id=movie_id, title=movie, overview=overview, poster_url=poster_url)
            movie.save()
            messages.success(request, f'"{movie}" added to your watchlist!')
            return render(request, 'movies_app/index.html')

        elif 'review' in request.POST:
            movie = Watchlist.objects.get(movie_id=request.POST['movie_id'])

            context = {
                'movie': movie,
            }
            return render(request, 'movies_app/review.html', context)

        elif 'review_new' in request.POST:
            title = request.POST['title']
            movie_id = request.POST['movie_id']
            overview = request.POST['overview']
            poster_url = f'https://image.tmdb.org/t/p/w500{request.POST["poster_url"]}'
            movie = {'title': title, 'movie_id': movie_id, 'overview': overview, 'poster_url': poster_url}

            context = {
                'movie': movie,
            }
            return render(request, 'movies_app/review.html', context)

        elif 'submit_review' in request.POST:
            movie_name = request.POST['title']
            movie_id = request.POST['movie_id']
            review_text = request.POST['text']
            rating = request.POST['rating']
            # remove from watchlist
            if Watchlist.objects.filter(movie_id=movie_id).exists():
                temp = Watchlist.objects.filter(movie_id=movie_id)
                overview = temp[0].overview
                temp.delete()
            else:
                overview = request.POST['overview']
            
            # check if movie already exists in seenlist
            if Seenlist.objects.filter(movie_id=movie_id).exists():
                messages.error(
                    request, f'"{movie_name}" already exists in your seenlist!')
                return render(request, 'movies_app/index.html')
            # add to seenlist
            review = Seenlist(movie_id=movie_id, title=movie_name,
                              review=review_text, rating=rating, date_watched=date.today(), overview=overview)
            review.save()
            
            messages.success(request, f'"{movie_name}" review added!')
            return render(request, 'movies_app/index.html')

        elif 'blog' in request.POST:
            reviews = Seenlist.objects.all().order_by('-date_watched')
            context = {
                'reviews': reviews,
            }
            return render(request, 'movies_app/blog.html', context)
        
        elif 'watchlist' in request.POST:
            movies = Watchlist.objects.all()
            context = {
                'movies': movies,
            }
            return render(request, 'movies_app/watchlist.html', context)

    return render(request, 'movies_app/index.html')


def roll():
    movie_to_watch = Watchlist.objects.order_by('?').first()
    movie_details = get_movie_info_by_id(movie_to_watch.movie_id)
    return movie_details


def get_movie_list(title: str):
    search = tmdb.Search()
    response = search.movie(query=title)
    return response['results'] if response['total_results'] > 0 else None


def get_movie_info_by_id(id: int):
    movie = tmdb.Movies(id)
    return movie.info() if movie else None
