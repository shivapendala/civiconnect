import pytest
from django.test import TestCase
from accounts.models import Municipality, User, CitizenProfile, CivicPoints, Badge, CitizenBadge
from accounts.gamification import award_points, get_leaderboard

class GamificationTests(TestCase):
    def setUp(self):
        self.municipality = Municipality.objects.create(name="Test City", state="Test State", country="Test Country")
        
        self.user1 = User.objects.create(email="citizen1@example.com", username="citizen1")
        self.citizen1 = CitizenProfile.objects.create(user=self.user1, municipality=self.municipality)
        
        self.user2 = User.objects.create(email="citizen2@example.com", username="citizen2")
        self.citizen2 = CitizenProfile.objects.create(user=self.user2, municipality=self.municipality)
        
        self.badge1 = Badge.objects.create(name="First Report", points_required=50)
        self.badge2 = Badge.objects.create(name="Community Hero", points_required=500)

    def test_award_points_and_level_up(self):
        # Initial points should be 0 (via get_or_create)
        result = award_points(self.citizen1, 40)
        self.assertEqual(result["new_total"], 40)
        self.assertEqual(result["current_level"], 1)
        self.assertFalse(result["leveled_up"])
        
        # Cross the 100 points threshold to level up
        result = award_points(self.citizen1, 70) # total 110
        self.assertEqual(result["new_total"], 110)
        self.assertEqual(result["current_level"], 2)
        self.assertTrue(result["leveled_up"])
        
    def test_badge_awarded(self):
        award_points(self.citizen1, 60) # Should award badge 1
        
        badges = CitizenBadge.objects.filter(citizen=self.citizen1)
        self.assertEqual(badges.count(), 1)
        self.assertEqual(badges.first().badge, self.badge1)
        
        # Award more points, should not duplicate badge 1, but should award badge 2 eventually
        award_points(self.citizen1, 500) # total 560
        badges = CitizenBadge.objects.filter(citizen=self.citizen1)
        self.assertEqual(badges.count(), 2)
        self.assertTrue(badges.filter(badge=self.badge2).exists())
        
    def test_leaderboard(self):
        award_points(self.citizen1, 100)
        award_points(self.citizen2, 300)
        
        leaderboard = get_leaderboard(limit=10, municipality=self.municipality)
        
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]["citizen_name"], "citizen2@example.com")
        self.assertEqual(leaderboard[0]["points"], 300)
        
        self.assertEqual(leaderboard[1]["citizen_name"], "citizen1@example.com")
        self.assertEqual(leaderboard[1]["points"], 100)

    def test_leaderboard_empty(self):
        leaderboard = get_leaderboard(limit=10, municipality=self.municipality)
        self.assertEqual(len(leaderboard), 0)

    def test_leaderboard_multiple_municipalities(self):
        muni2 = Municipality.objects.create(name="Other City", state="OS", country="OC")
        user3 = User.objects.create(email="c3@example.com", username="c3")
        citizen3 = CitizenProfile.objects.create(user=user3, municipality=muni2)
        
        award_points(self.citizen1, 100)
        award_points(citizen3, 500)
        
        leaderboard = get_leaderboard(limit=10, municipality=self.municipality)
        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0]["citizen_name"], "citizen1@example.com")

# (End of test file)
