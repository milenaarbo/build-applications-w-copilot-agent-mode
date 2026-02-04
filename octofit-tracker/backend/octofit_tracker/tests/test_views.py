from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from octofit_tracker.models import Team, Activity


class IndexViewAggregationTest(TestCase):
    def test_index_sums_duration_per_team_and_orders(self):
        User = get_user_model()
        u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        u2 = User.objects.create_user(username='u2', email='u2@example.com', password='pass')

        t1 = Team.objects.create(name='Team A')
        t2 = Team.objects.create(name='Team B')

        t1.members.add(u1)
        t2.members.add(u2)

        Activity.objects.create(user=u1, activity_type='run', duration_min=30, timestamp=timezone.now())
        Activity.objects.create(user=u1, activity_type='cycle', duration_min=20, timestamp=timezone.now())
        Activity.objects.create(user=u2, activity_type='run', duration_min=10, timestamp=timezone.now())

        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

        teams = list(resp.context['teams'])
        # Team A total = 50, Team B total = 10
        self.assertEqual(teams[0].name, 'Team A')
        self.assertEqual(teams[0].total_minutes, 50)
        self.assertEqual(teams[1].total_minutes, 10)


class ActivityFormViewTest(TestCase):
    def test_get_activity_form_renders(self):
        User = get_user_model()
        User.objects.create_user(username='u1', email='u1@example.com', password='pass')

        resp = self.client.get(reverse('activity_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('form', resp.context)

    def test_post_activity_creates_activity_and_redirects(self):
        User = get_user_model()
        u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        team = Team.objects.create(name='Team X')

        data = {
            'user': u1.pk,
            'team': team.pk,
            'activity_type': 'run',
            'duration_min': 42,
        }
        resp = self.client.post(reverse('activity_create'), data)
        # redirect back to ranking
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse('home'))

        act = Activity.objects.filter(user=u1, duration_min=42).first()
        self.assertIsNotNone(act)
        # user should have been added to the team by the view
        self.assertTrue(team.members.filter(pk=u1.pk).exists())
