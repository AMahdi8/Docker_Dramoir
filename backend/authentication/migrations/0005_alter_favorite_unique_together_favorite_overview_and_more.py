# Generated by Django 5.1.4 on 2025-04-10 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_profile_picture_favorite'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'content_id')},
        ),
        migrations.AddField(
            model_name='favorite',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='poster_path',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='favorite',
            name='vote_average',
            field=models.FloatField(default=0),
        ),
    ]
