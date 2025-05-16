from django.db import models
from django.core.exceptions import ValidationError


class SiteSetting(models.Model):
    download_domain = models.CharField(
        max_length=255,
        help_text="domain that use for donwload links (example: ps://example.com)"
    )

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Setting"

    def __str__(self):
        return self.download_domain

    def save(self, *args, **kwargs):

        if not self.pk and SiteSetting.objects.exists():
             raise ValueError("Only one record allowed")

        super().save(*args, **kwargs)



class Country(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class Crew(models.Model):
    ROLE_CHOICES = (
        ('A', 'Actor'),
        ('D', 'Director'),
        ('W', 'Writer'),
        ('O', 'Other')
    )
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    bio = models.TextField()
    # birth_date = models.DateField()
    birth_year = models.IntegerField()
    image = models.ImageField(
        upload_to='images/crews/',
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='actors',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Movie(models.Model):
    AGE_CATEGORY_CHOICES = (
        ('G', 'General Audiences(G)'),
        ('PG', 'Parental Guidance Suggested(PG)'),
        ('PG-13', 'Parents Strongly Cautioned(PG-13)'),
        ('R', 'Restricted(R)'),
        ('NC-17', 'Adults Only(NC-17)')
    )
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(
        null=True,
        blank=True
    )
    duration = models.IntegerField(null=True, blank=True)
    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField(
        null=True,
        blank=True
    )
    imdb_rank = models.IntegerField(
        null=True,
        blank=True
    )
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )
    image = models.ImageField(
        upload_to='images/movie/',
        null=True,
        blank=True
    )
    countries = models.ManyToManyField(
        Country,
        related_name='movies',
        blank=True
    )
    languages = models.ManyToManyField(
        Language,
        related_name='movies',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='movies',
        blank=True
    )
    crews = models.ManyToManyField(
        Crew,
        related_name='movies',
        blank=True
    )
    subtitle_link = models.TextField(
        null=True,
        blank=True
    )
    trailer_link = models.TextField(
        null=True,
        blank=True
    )
    choosen_home_page = models.BooleanField(default=False)
    trend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        ratings = self.comments.exclude(
            rating=None).values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else None

    @property
    def comments_count(self):
        return self.comments.count()


    def save(self, *args, **kwargs):
        if self.trend:
            selected_movie = Movie.objects.filter(
                trend=True).exclude(pk=self.pk).count()
            selected_series = Series.objects.filter(
                trend=True).count()

            if selected_series + selected_movie >= 5:
                raise ValidationError(
                    f"You can't choose more than 5 movie and series for home page trend\n please remove those you don't want, then add others"
                )

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} {self.release_year}'


class Series(models.Model):
    AGE_CATEGORY_CHOICES = (
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only')
    )
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    end_date = models.IntegerField(
        null=True,
        blank=True
    )
    age_category = models.CharField(max_length=5, choices=AGE_CATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField(
        null=True,
        blank=True
    )
    imdb_rank = models.IntegerField(
        null=True,
        blank=True
    )
    rate = models.DecimalField(
        max_digits=3,
        decimal_places=1,
    )
    image = models.ImageField(
        upload_to='images/series/',
        null=True,
        blank=True
    )
    countries = models.ManyToManyField(
        Country,
        related_name='series',
        blank=True
    )
    languages = models.ManyToManyField(
        Language,
        related_name='series',
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name='series',
        blank=True
    )
    crews = models.ManyToManyField(
        Crew,
        related_name='series',
        blank=True
    )

    choosen_home_page = models.BooleanField(default=False)
    trend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        ratings = self.comments.exclude(
            rating=None).values_list('rating', flat=True)
        return sum(ratings) / len(ratings) if ratings else None

    @property
    def comments_count(self):
        return self.comments.count()

    def save(self, *args, **kwargs):
        if self.trend:
            selected_movie = Movie.objects.filter(
                trend=True).count()
            selected_series = Series.objects.filter(
                trend=True).exclude(pk=self.pk).count()

            if selected_series + selected_movie >= 5:
                raise ValidationError(
                    f"You can't choose more than 5 movie and series for home page trend\n please remove those you don't want, then add others"
                )

        return super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class Season(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    number = models.IntegerField()

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='seasons'
    )
    release_year = models.IntegerField(
        null=True,
        blank=True
    )
    is_finished = models.BooleanField(default=False)
    description = models.TextField(
        null=True,
        blank=True
    )
    trailer_link = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def avg_duration(self):
        episode_durations = self.episodes.exclude(
            duration=None).values_list('duration', flat=True)
        return sum(episode_durations) / len(episode_durations) if episode_durations else None

    def __str__(self):
        season = str(self.number).zfill(3)
        return f"{self.series}: {self.title or ''} (S{season})"


class Episode(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='episodes',
    )
    number = models.IntegerField()
    duration = models.IntegerField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    subtitle_link = models.TextField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        season = str(self.season.number).zfill(3)
        episode = str(self.number).zfill(3)
        return f"{self.season.series}: {self.title or ''} (S{season}E{episode})"


class DownloadFile(models.Model):
    class QualityChoices(models.TextChoices):
        # Standard Definition
        P144 = '144p', '144p'
        P240 = '240p', '240p'
        P360 = '360p', '360p'
        P480 = '480p', '480p'
        p540 = '540p', '540p'
        # High Definition
        P720 = '720p', '720p'
        P1080 = '1080p', '1080p'
        # Ultra High Definition
        P1440 = '1440p', '1440p'
        P2160 = '2160p', '2160p'
        P4320 = '4320p', '4320p'

    SOURCE_CHOICES = [
        ('Blu-ray', 'Blu-ray'),  # Best overall quality, often lossless
        ('WEB-DL', 'WEB-DL'),    # High quality, sourced directly from online services
        ('WEBRip', 'WEBRip'),    # Lower quality than WEB-DL, encoded from streams
        # High Definition Rip, good but not as clean as WEB-DL
        ('HDRip', 'HDRip'),
        ('BRRip', 'BRRip'),      # Blu-ray re-encoded, lower quality than Blu-ray
        # Recorded directly from TV, may have ads or watermarks
        ('HDTV', 'HDTV'),
        ('DVD-Rip', 'DVD-Rip'),  # Lower resolution, compressed from DVDs
        ('TS', 'TS'),            # Telesync, often cam-sourced with synced audio
        ('CAM', 'CAM'),          # Filmed using a camera in theaters, lowest quality
    ]

    FILE_FORMAT_CHOICES = [
        ('MP4', 'MP4'),
        ('FLV', 'FLV'),
        ('MOV', 'MOV'),
        ('MKV', 'MKV'),
        ('LXF', 'LXF'),
        ('MXF', 'MXF'),
        ('AVI', 'AVI'),
        ('QuickTime', 'QuickTime'),
        ('WebM', 'WebM'),
    ]

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='download_urls',
        null=True,
        blank=True
    )
    episode = models.ForeignKey(
        Episode,
        on_delete=models.CASCADE,
        related_name='download_urls',
        null=True,
        blank=True
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='WEB-DL',
        help_text="Source of the video file."
    )
    file_format = models.CharField(
        max_length=20,
        choices=FILE_FORMAT_CHOICES,
        default='MKV',
        help_text="File container format."
    )
    sticky_subtitles = models.BooleanField()
    quality = models.CharField(
        max_length=20,
        choices=QualityChoices.choices
    )
    _256_bit_encryption = models.BooleanField(
        default=False, name='256-bit-encryption')
    _10_bit_variants = models.BooleanField(
        default=False, name='10-bit-variant')
    download_url = models.TextField(
        null=True,
        blank=True
    )
    file_size = models.IntegerField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        context = f"Movie: {self.movie.title}"\
            if self.movie\
            else f"Episode: {self.episode.title} (S{self.episode.season}E{self.episode.number})" \
            if self.episode\
            else "No Context"

        return f"{context} | Quality: {self.quality}"

    def save(self, *args, **kwargs):
        if not self.episode and not self.movie:
            raise ValueError(
                "Download File must be associated with either a movie or a series.")
        if self.episode and self.movie:
            raise ValueError(
                "Download File cannot be associated with both a movie and a series simultaneously.")
        return super().save(*args, **kwargs)

class WeeklySchedule(models.Model):
    DAY_CHOICES = (
        ('monday', 'دوشنبه'),
        ('tuesday', 'سه‌شنبه'),
        ('wednesday', 'چهارشنبه'),
        ('thursday', 'پنج‌شنبه'),
        ('friday', 'جمعه'),
        ('saturday', 'شنبه'),
        ('sunday', 'یک‌شنبه'),
    )
    
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='weekly_schedules',
        verbose_name='Series'
    )
    
    day_of_week = models.CharField(
        max_length=10,
        choices=DAY_CHOICES,
        verbose_name='Day of Week'
    )
    
    air_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Air Time'
    )
    
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Notes'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Weekly Schedule'
        verbose_name_plural = 'Weekly Schedules'
        unique_together = ('series', 'day_of_week')
        ordering = ['day_of_week']
    
    def __str__(self):
        return f"{self.series.title} - {self.get_day_of_week_display()}"


class ShortDescription(models.Model):
    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name='short_descriptions',
        verbose_name='Series'
    )
    
    description = models.TextField(
        verbose_name='Short Description'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Short Description'
        verbose_name_plural = 'Short Descriptions'
    
    def __str__(self):
        return f"Short Description for {self.series.title}"

class WatchHistory(models.Model):
    MOVIE = 'movie'
    SERIES = 'series'
    CONTENT_TYPE_CHOICES = [
        (MOVIE, 'Movie'),
        (SERIES, 'Series'),
    ]

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='watch_history')
    content_id = models.IntegerField()  # ID of the movie or series
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    country = models.CharField(max_length=100)  # Country of the content
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'content_id', 'content_type']
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user.username} watched {self.content_type} {self.content_id}"
