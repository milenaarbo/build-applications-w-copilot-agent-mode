from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # make email unique as required
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username or self.email


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField('User', related_name='teams', blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ("run", "Run"),
        ("cycle", "Cycle"),
        ("swim", "Swim"),
        ("workout", "Workout"),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=32, choices=ACTIVITY_CHOICES)
    duration_min = models.PositiveIntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.activity_type} @ {self.timestamp}"


class Workout(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    creator = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='workouts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LeaderboardEntry(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='leaderboard_entries')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='leaderboard_entries')
    score = models.IntegerField(default=0)
    rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user} ({self.team}) - {self.score}"