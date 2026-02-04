from rest_framework import serializers, viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Team, Activity, Workout, LeaderboardEntry

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'members']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'activity_type', 'duration_min', 'distance_km', 'timestamp']


class WorkoutSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'creator', 'created_at']


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user', 'team', 'score', 'rank']


# --- viewsets ---
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.prefetch_related('members').all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('user').all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.select_related('creator').all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.AllowAny]


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum

class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Soma dos minutos de atividades por equipe
        teams = Team.objects.all()
        leaderboard = []
        for team in teams:
            total = Activity.objects.filter(user__teams=team).aggregate(total_minutes=Sum('duration_min'))['total_minutes'] or 0
            leaderboard.append({
                'team': team.name,
                'total_minutes': total
            })
        leaderboard = sorted(leaderboard, key=lambda x: x['total_minutes'], reverse=True)
        return Response(leaderboard)
