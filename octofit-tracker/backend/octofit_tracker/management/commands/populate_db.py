from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from octofit_tracker.models import Team, Activity, Workout, LeaderboardEntry
from datetime import timedelta
from pymongo import MongoClient, errors


User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        now = timezone.now()

        self.stdout.write('Deleting existing data (ORM)...')
        LeaderboardEntry.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        # remove all users (tests require a clean slate)
        User.objects.all().delete()

        self.stdout.write('Creating users and teams (ORM)...')
        # Marvel
        im = User.objects.create_user(username='ironman', email='tony@stark.com', password='password', first_name='Tony', last_name='Stark')
        sp = User.objects.create_user(username='spiderman', email='peter@parker.com', password='password', first_name='Peter', last_name='Parker')
        hk = User.objects.create_user(username='hulk', email='bruce@banner.com', password='password', first_name='Bruce', last_name='Banner')

        # DC
        bm = User.objects.create_user(username='batman', email='bruce@wayne.com', password='password', first_name='Bruce', last_name='Wayne')
        sm = User.objects.create_user(username='superman', email='clark@kent.com', password='password', first_name='Clark', last_name='Kent')
        ww = User.objects.create_user(username='wonder_woman', email='diana@prince.com', password='password', first_name='Diana', last_name='Prince')

        marvel = Team.objects.create(name='marvel')
        dc = Team.objects.create(name='dc')
        marvel.members.add(im, sp, hk)
        dc.members.add(bm, sm, ww)

        self.stdout.write('Creating activities, workouts and leaderboard entries (ORM)...')
        # sample activities
        Activity.objects.create(user=im, activity_type='run', duration_min=30, distance_km=5.0, timestamp=now - timedelta(days=1))
        Activity.objects.create(user=sp, activity_type='run', duration_min=45, distance_km=8.2, timestamp=now - timedelta(days=2))
        Activity.objects.create(user=hk, activity_type='workout', duration_min=60, timestamp=now - timedelta(hours=5))
        Activity.objects.create(user=bm, activity_type='cycle', duration_min=50, distance_km=20.0, timestamp=now - timedelta(days=3))
        Activity.objects.create(user=sm, activity_type='swim', duration_min=40, distance_km=2.5, timestamp=now - timedelta(days=4))
        Activity.objects.create(user=ww, activity_type='workout', duration_min=55, timestamp=now - timedelta(days=1, hours=2))

        # workouts
        Workout.objects.create(name='Stark HIIT', description='High intensity interval training', creator=im)
        Workout.objects.create(name='Wayne Strength', description='Strength routine', creator=bm)

        # leaderboard
        LeaderboardEntry.objects.create(user=im, team=marvel, score=980)
        LeaderboardEntry.objects.create(user=sp, team=marvel, score=860)
        LeaderboardEntry.objects.create(user=hk, team=marvel, score=640)
        LeaderboardEntry.objects.create(user=bm, team=dc, score=920)
        LeaderboardEntry.objects.create(user=sm, team=dc, score=940)
        LeaderboardEntry.objects.create(user=ww, team=dc, score=870)

        self.stdout.write(self.style.SUCCESS('ORM data created — now ensuring MongoDB-level indexes...'))

        # Ensure unique index on email at DB level as requested
        try:
            client = MongoClient('mongodb://localhost:27017')
            db = client['octofit_db']
            db.users.create_index([('email', 1)], unique=True)
            self.stdout.write(self.style.SUCCESS('Ensured unique index on users.email'))
        except errors.PyMongoError as exc:
            self.stdout.write(self.style.WARNING(f'Could not create index via pymongo: {exc}'))

        # show counts
        counts = {
            'users': User.objects.count(),
            'teams': Team.objects.count(),
            'activities': Activity.objects.count(),
            'workouts': Workout.objects.count(),
            'leaderboard': LeaderboardEntry.objects.count(),
        }
        for k, v in counts.items():
            self.stdout.write(f'{k}: {v}')

        self.stdout.write(self.style.SUCCESS('octofit_db population complete'))
