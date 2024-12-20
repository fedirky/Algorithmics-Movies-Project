from django.core.management.base import BaseCommand
from django.db import transaction
import csv

from movies.models import Movie, MovieGenre, MovieDirector, MovieStar

class Command(BaseCommand):
    help = "Imports movie data into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', type=str, required=True,
            help='Path to the CSV file containing movie data.'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        skipped_rows = 0  # Counter for skipped rows
        
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                with transaction.atomic():
                    for row in reader:
                        # Check for empty fields
                        if any(not row[field] for field in ['movie_id', 'movie_name', 'description', 'year', 
                                                            'certificate', 'runtime', 'rating', 'votes', 
                                                            'genre', 'director', 'star']):
                            skipped_rows += 1
                            continue
                        
                        # Process Genres
                        genre_names = row['genre'].split(', ')
                        genres = []
                        for genre_name in genre_names:
                            genre, created = MovieGenre.objects.get_or_create(name=genre_name)
                            genres.append(genre)
                        
                        # Process Directors
                        director_names = row['director'].split(', ')
                        directors = []
                        for director_name in director_names:
                            director, created = MovieDirector.objects.get_or_create(name=director_name)
                            directors.append(director)
                        
                        # Process Stars
                        star_names = row['star'].split(', ')
                        stars = []
                        for star_name in star_names:
                            star, created = MovieStar.objects.get_or_create(name=star_name)
                            stars.append(star)
                        
                        # Create Movie instance
                        movie, created = Movie.objects.get_or_create(
                            movie_id=row['movie_id'],
                            defaults={
                                'movie_name': row['movie_name'],
                                'description': row['description'],
                                'year': int(row['year']),
                                'certificate': row['certificate'],
                                'runtime': int(row['runtime'].split()[0]),
                                'rating': float(row['rating']),
                                'votes': int(row['votes'].split('.')[0]),
                            }
                        )
                        
                        # Add Many-to-Many relationships
                        if created:
                            movie.genres.set(genres)
                            movie.directors.set(directors)
                            movie.stars.set(stars)
                        
                        self.stdout.write(self.style.SUCCESS(f"Successfully imported movie: {movie.movie_name}"))

            self.stdout.write(self.style.WARNING(f"Skipped {skipped_rows} rows due to missing data."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
