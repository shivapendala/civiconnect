from .models import CivicPoints, Badge, CitizenBadge
from django.db import transaction

def award_points(citizen_profile, amount, reason=""):
    """
    Award points to a citizen and check for new badges.
    """
    with transaction.atomic():
        points_record, created = CivicPoints.objects.get_or_create(citizen=citizen_profile)
        
        old_level = points_record.level
        points_record.add_points(amount)
        new_level = points_record.level
        
        # Check for new badges
        available_badges = Badge.objects.filter(points_required__lte=points_record.total_points)
        for badge in available_badges:
            CitizenBadge.objects.get_or_create(citizen=citizen_profile, badge=badge)
            
        return {
            "points_awarded": amount,
            "new_total": points_record.total_points,
            "leveled_up": new_level > old_level,
            "current_level": new_level
        }

def get_leaderboard(limit=10, municipality=None):
    """
    Get top citizens by points.
    """
    query = CivicPoints.objects.select_related('citizen__user')
    if municipality:
        query = query.filter(citizen__municipality=municipality)
        
    top_records = query.order_by('-total_points')[:limit]
    
    leaderboard = []
    for rank, record in enumerate(top_records, 1):
        leaderboard.append({
            "rank": rank,
            "citizen_name": record.citizen.user.email, # normally would use full_name
            "points": record.total_points,
            "level": record.level
        })
        
    return leaderboard
