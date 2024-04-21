# Generated by Django 5.0.4 on 2024-04-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies_app", "0003_rename_watched_movie_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="movie_id",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="movie",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
