# Generated by Django 5.0.4 on 2024-04-21 02:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies_app", "0002_movie_review_movie_watched"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="watched",
            new_name="seen",
        ),
    ]
