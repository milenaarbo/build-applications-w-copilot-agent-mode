from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Team, Activity, Workout, LeaderboardEntry

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff')
    search_fields = ('username', 'email')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'activity_type', 'duration_min', 'timestamp')
    search_fields = ('user__username', 'activity_type')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'created_at')


@admin.register(LeaderboardEntry)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'score', 'rank')
    ordering = ('-score',)
