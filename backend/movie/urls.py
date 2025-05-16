from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('movie', MovieViewSet, basename='movie')
router.register('series', SeriesViewSet, basename='series')
router.register('country', CountryViewSet, basename='country')
router.register('genre', GenreViewSet, basename='genre')
router.register('language', LanguageViewSet, basename='language')
router.register('home', MoreSeriesViewSet, basename='home_series')
router.register('home', MoreMovieViewSet, basename='home_movies')

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('weeklist/', WeeklyScheduleListView.as_view(), name='weekly-schedule-list'),
    path('shortdescription/<int:id>/', ShortDescriptionView.as_view(), name='short-description'),
    path('home/', HomePageView.as_view(), name='home'),
    path('watch-history/', WatchHistoryView.as_view(), name='watch-history'),
    path('watch-history/stats/', WatchHistoryStatsView.as_view(), name='watch-history-stats'),
] + router.urls
