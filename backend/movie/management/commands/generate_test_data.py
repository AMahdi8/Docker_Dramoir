from django.core.management.base import BaseCommand
from django.utils import timezone
from movie.models import Movie, Series, Genre
import random
from datetime import datetime, timedelta
import requests

class Command(BaseCommand):
    help = 'Generates test data for movies and series'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of movies/series to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        
        # TMDB API configuration
        api_key = "YOUR_TMDB_API_KEY"  # Replace with your TMDB API key
        base_url = "https://api.themoviedb.org/3"
        
        # Create genres
        genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime",
            "Documentary", "Drama", "Family", "Fantasy", "History",
            "Horror", "Music", "Mystery", "Romance", "Science Fiction",
            "Thriller", "War", "Western"
        ]
        
        genre_objects = []
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genre_objects.append(genre)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(genre_objects)} genres'))

        # Generate Movies
        movies_created = 0
        page = 1
        while movies_created < count:
            try:
                # Fetch popular movies from TMDB
                response = requests.get(
                    f"{base_url}/movie/popular",
                    params={
                        "api_key": api_key,
                        "page": page
                    }
                )
                data = response.json()
                
                for movie_data in data.get('results', []):
                    if movies_created >= count:
                        break
                        
                    # Create movie
                    movie = Movie.objects.create(
                        title=movie_data['title'],
                        overview=movie_data['overview'],
                        release_date=movie_data['release_date'],
                        poster_path=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
                        backdrop_path=f"https://image.tmdb.org/t/p/original{movie_data['backdrop_path']}",
                        vote_average=movie_data['vote_average'],
                        vote_count=movie_data['vote_count'],
                        popularity=movie_data['popularity'],
                        tmdb_id=movie_data['id']
                    )
                    
                    # Add random genres
                    movie_genres = random.sample(genre_objects, random.randint(1, 3))
                    movie.genres.set(movie_genres)
                    
                    movies_created += 1
                    self.stdout.write(f'Created movie: {movie.title}')
                
                page += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                break

        # Generate Series
        series_created = 0
        page = 1
        while series_created < count:
            try:
                # Fetch popular TV shows from TMDB
                response = requests.get(
                    f"{base_url}/tv/popular",
                    params={
                        "api_key": api_key,
                        "page": page
                    }
                )
                data = response.json()
                
                for series_data in data.get('results', []):
                    if series_created >= count:
                        break
                        
                    # Create series
                    series = Series.objects.create(
                        title=series_data['name'],
                        overview=series_data['overview'],
                        first_air_date=series_data.get('first_air_date'),
                        poster_path=f"https://image.tmdb.org/t/p/w500{series_data['poster_path']}",
                        backdrop_path=f"https://image.tmdb.org/t/p/original{series_data['backdrop_path']}",
                        vote_average=series_data['vote_average'],
                        vote_count=series_data['vote_count'],
                        popularity=series_data['popularity'],
                        tmdb_id=series_data['id'],
                        number_of_seasons=random.randint(1, 5),
                        number_of_episodes=random.randint(10, 100),
                        status=random.choice(['Ended', 'Running'])
                    )
                    
                    # Add random genres
                    series_genres = random.sample(genre_objects, random.randint(1, 3))
                    series.genres.set(series_genres)
                    
                    series_created += 1
                    self.stdout.write(f'Created series: {series.title}')
                
                page += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                break

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {movies_created} movies and {series_created} series'
        )) 