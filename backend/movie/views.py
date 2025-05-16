from django.http import HttpResponseRedirect
from django.db.models import F, Max, Subquery, OuterRef, Q, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.decorators import action
from itsdangerous import BadSignature, SignatureExpired  # type: ignore
from django.utils.timezone import now
from datetime import timedelta
from random import sample
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework import generics
from .models import Country, DownloadFile, Genre, Language, Movie, Series, WeeklySchedule, ShortDescription, WatchHistory
from .serializers import CountrySerializer, GenreSerializer, LanguageSerializer, MovieDetailSerializer, MovieListSerializer, SeriesDetailSerializer, SeriesListSerializer, WeeklyScheduleSerializer, ShortDescriptionSerializer, WatchHistorySerializer, WatchHistoryCreateSerializer, WatchHistoryStatsSerializer
from .utilities import get_movies_and_series_by_country


class HomePageView(APIView):
    def get(self, request):
        trend_movies = Movie.objects.filter(trend=True)
        trend_series = Series.objects.filter(trend=True)

        choosen_korean_movie = Movie.objects.filter(
            choosen_home_page=True, countries__name__in=["South Korea"])
        choosen_movie = Movie.objects.filter(choosen_home_page=True).exclude(
            countries__name__in=["South Korea"])

        choosen_korean_series = Series.objects.filter(
            choosen_home_page=True, countries__name__in=['South Korea'])
        best_korean_series = Series.objects.filter(
	    choosen_home_page=False,
            countries__name__in=['South Korea']).order_by('-rate')[:6]
        best_chineas_series = Series.objects.filter(
            choosen_home_page=False,
	    countries__name__in=['China']).order_by('-rate')[:6]
        best_series = Series.objects.filter(choosen_home_page=False).exclude(
	    countries__name__in=['South Korea', 'China']).order_by('-rate')[:6]

        random_movies = sample(list(choosen_movie), min(len(choosen_movie), 8))
        random_korean_movies = sample(
            list(choosen_korean_movie), min(len(choosen_korean_movie), 8))
        random_korean_series = sample(
            list(choosen_korean_series), min(len(choosen_korean_series), 6))

        return Response({
            'trend_movies': MovieListSerializer(trend_movies, many=True).data,
            'trend_series': SeriesListSerializer(trend_series, many=True).data,
            'choosen_korean_movie': MovieListSerializer(random_korean_movies, many=True).data,
            'choosen_movie': MovieListSerializer(random_movies, many=True).data,
            'choosen_korean_series': SeriesListSerializer(random_korean_series, many=True).data,
            'best_korean_series': SeriesListSerializer(best_korean_series, many=True).data,
            'best_chineas_series': SeriesListSerializer(best_chineas_series, many=True).data,
            'best_series': SeriesListSerializer(best_series, many=True).data
        })
class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({"results": []})

        movies = Movie.objects.filter(title__icontains=query)

        series = Series.objects.filter(title__icontains=query)

        movie_serializer = MovieListSerializer(movies, many=True)
        series_serializer = SeriesListSerializer(series, many=True)

        results = {
            "movies": movie_serializer.data,
            "series": series_serializer.data
        }

        return Response(results)

class MoreSeriesViewSet(ListModelMixin, GenericViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesListSerializer

    @action(detail=False, methods=['get'], url_path='best_series', )
    def best(self, request):
        best_series = self.get_queryset().filter(choosen_home_page=False).exclude(
            countries__name__in=['South Korea', 'China']).order_by('-rate')
        page = self.paginate_queryset(best_series)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='best_chineas_series')
    def best_chinese(self, request):
        best_chinese_series = self.get_queryset().filter(
	    choosen_home_page=False,
            countries__name='China').order_by('-rate')
        page = self.paginate_queryset(best_chinese_series)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='best_korean_series')
    def best_korean(self, request):
        best_korean_series = self.get_queryset().filter(
            choosen_home_page=False,
	    countries__name='South Korea').order_by('-rate')
        page = self.paginate_queryset(best_korean_series)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='choosen_korean_series')
    def choosen_korean(self, request):
        choosen_korean_series = self.get_queryset().filter(
            choosen_home_page=True, countries__name='South Korea')
        page = self.paginate_queryset(choosen_korean_series)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class MoreMovieViewSet(ListModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer

    @action(detail=False, methods=['get'], url_path='choosen_movies')
    def choosen(self, request):
        choosen_movie = self.get_queryset().filter(
            choosen_home_page=True).exclude(countries__name='South Korea')
        page = self.paginate_queryset(choosen_movie)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='choosen_korean_movies')
    def choosen_korean(self, request):
        choosen_korean_movie = self.get_queryset().filter(
            choosen_home_page=True, countries__name='South Korea')
        page = self.paginate_queryset(choosen_korean_movie)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Movie.objects.prefetch_related(
        'countries', 'languages', 'genres', 'download_urls'
    ).annotate(
        highest_quality=Subquery(
            DownloadFile.objects.filter(movie=OuterRef('pk'))
            .order_by('source', '-quality')
            .values('quality')[:1]
        ),
        highest_source=Subquery(
            DownloadFile.objects.filter(movie=OuterRef('pk'))
            .order_by('source', '-quality')
            .values('source')[:1]
        )
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer


class SeriesViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    GenericViewSet):

    def get_queryset(self):
        if self.action == 'list':
            return Series.objects.prefetch_related(
                'countries', 'languages', 'genres').all()
        return Series.objects.prefetch_related(
            'countries', 'languages', 'genres',
            'seasons', 'seasons__episodes',
            'seasons__episodes__download_urls').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SeriesListSerializer
        return SeriesDetailSerializer


class CountryViewSet(RetrieveModelMixin,
                     GenericViewSet):
    queryset = Country.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = CountrySerializer
    lookup_field = 'name'


class LanguageViewSet(RetrieveModelMixin,
                      GenericViewSet):
    queryset = Language.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = LanguageSerializer
    lookup_field = 'name'


class GenreViewSet(RetrieveModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.prefetch_related(
        'series', 'movies').all()
    serializer_class = GenreSerializer
    lookup_field = 'name'

class WeeklyScheduleListView(generics.ListAPIView):
    queryset = WeeklySchedule.objects.filter(is_active=True).select_related('series')
    serializer_class = WeeklyScheduleSerializer
    pagination_class = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        day = self.request.query_params.get('day', None)
        
        if day:
            queryset = queryset.filter(day_of_week=day)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Group by days if no specific day is requested
        if not request.query_params.get('day'):
            schedule_by_day = {}
            for day, day_name in WeeklySchedule.DAY_CHOICES:
                day_schedules = queryset.filter(day_of_week=day)
                if day_schedules.exists():
                    serializer = self.get_serializer(day_schedules, many=True)
                    schedule_by_day[day] = {
                        'day_name': day_name,
                        'schedules': serializer.data
                    }
            
            return Response(schedule_by_day)
        
        # Normal list response for specific day filter
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShortDescriptionView(generics.RetrieveAPIView):
    serializer_class = ShortDescriptionSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return ShortDescription.objects.filter(is_active=True)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class WatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watch_history = WatchHistory.objects.filter(user=request.user)
        serializer = WatchHistorySerializer(watch_history, many=True)
        return Response(serializer.data)

    def post(self, request):
        content_type = request.data.get('content_type')
        content_id = request.data.get('content_id')

        if not content_type or not content_id:
            return Response(
                {'error': 'content_type and content_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if content_type == 'movie':
                content = Movie.objects.get(id=content_id)
                # Get the first country from the countries list
                country = content.countries.first().name if content.countries.exists() else None
            elif content_type == 'series':
                content = Series.objects.get(id=content_id)
                # Get the first country from the countries list
                country = content.countries.first().name if content.countries.exists() else None
            else:
                return Response(
                    {'error': 'Invalid content_type'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            watch_history, created = WatchHistory.objects.get_or_create(
                user=request.user,
                content_type=content_type,
                content_id=content_id,
                defaults={'country': country}
            )

            if not created:
                watch_history.country = country
                watch_history.save()

            serializer = WatchHistorySerializer(watch_history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (Movie.DoesNotExist, Series.DoesNotExist):
            return Response(
                {'error': f'{content_type} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        """Remove a movie/series from watch history"""
        serializer = WatchHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                watch_history = WatchHistory.objects.get(
                    user=request.user,
                    content_id=serializer.validated_data['content_id'],
                    content_type=serializer.validated_data['content_type']
                )
                watch_history.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except WatchHistory.DoesNotExist:
                return Response(
                    {'error': 'Content not found in watch history'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchHistoryStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's watch history statistics"""
        # Get total counts
        total_movies = WatchHistory.objects.filter(
            user=request.user,
            content_type='movie'
        ).count()
        
        total_series = WatchHistory.objects.filter(
            user=request.user,
            content_type='series'
        ).count()

        # Get counts by country
        movies_by_country = dict(WatchHistory.objects.filter(
            user=request.user,
            content_type='movie'
        ).values('country').annotate(count=Count('id')).values_list('country', 'count'))

        series_by_country = dict(WatchHistory.objects.filter(
            user=request.user,
            content_type='series'
        ).values('country').annotate(count=Count('id')).values_list('country', 'count'))

        data = {
            'total_movies': total_movies,
            'total_series': total_series,
            'movies_by_country': movies_by_country,
            'series_by_country': series_by_country
        }

        serializer = WatchHistoryStatsSerializer(data)
        return Response(serializer.data)
