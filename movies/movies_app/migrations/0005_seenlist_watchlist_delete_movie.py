# Generated by Django 5.0.4 on 2024-04-24 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movies_app", "0004_movie_movie_id_alter_movie_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Seenlist",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("movie_id", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=100)),
                ("review", models.TextField(default="")),
                ("rating", models.IntegerField(default=0)),
                ("date_watched", models.DateField(default="1999-08-29")),
            ],
        ),
        migrations.CreateModel(
            name="Watchlist",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("movie_id", models.IntegerField(default=0)),
                ("title", models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="Movie",
        ),
    ]
