from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth, TruncDay
from .models import Complaint, ComplaintStatus, Feedback
from accounts.models import StaffProfile

def get_complaint_analytics():
    """
    Returns aggregated data for complaint trends and distribution.
    """
    # Distribution by Category
    category_distribution = list(
        Complaint.objects.values('category__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    # Distribution by Priority
    priority_distribution = list(
        Complaint.objects.values('priority')
        .annotate(count=Count('id'))
        .order_by('priority')
    )
    
    # Complaints per day (last 30 days)
    # Using TruncDay for grouping
    daily_trend = list(
        Complaint.objects.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('-day')[:30]
    )

    return {
        'category_distribution': category_distribution,
        'priority_distribution': priority_distribution,
        'daily_trend': daily_trend,
    }

def get_performance_analytics():
    """
    Returns aggregated data for department and staff performance.
    """
    # Average Resolution Time for CLOSED/CITIZEN_VERIFIED complaints
    # Requires tracking the exact time of resolution (using updated_at as proxy for simplicity)
    resolved_complaints = Complaint.objects.filter(
        status__in=[ComplaintStatus.CITIZEN_VERIFIED, ComplaintStatus.CLOSED, ComplaintStatus.RESOLVED]
    ).annotate(
        resolution_time=ExpressionWrapper(
            F('updated_at') - F('created_at'),
            output_field=DurationField()
        )
    )
    avg_resolution = resolved_complaints.aggregate(avg=Avg('resolution_time'))['avg']

    # Reopened complaints count
    reopened_count = Complaint.objects.filter(status=ComplaintStatus.REOPENED).count()

    # Workload per department
    dept_workload = list(
        Complaint.objects.filter(status__in=[ComplaintStatus.ASSIGNED, ComplaintStatus.IN_PROGRESS])
        .values('category__department__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    return {
        'avg_resolution_hours': avg_resolution.total_seconds() / 3600 if avg_resolution else 0,
        'reopened_count': reopened_count,
        'department_active_workload': dept_workload,
    }

def get_citizen_analytics():
    """
    Returns aggregated data for citizen satisfaction and feedback.
    """
    # Average feedback score
    avg_score = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    # Satisfaction rate (percentage of feedbacks 4 stars and above)
    total_feedbacks = Feedback.objects.count()
    if total_feedbacks > 0:
        satisfied = Feedback.objects.filter(rating__gte=4).count()
        satisfaction_rate = (satisfied / total_feedbacks) * 100
    else:
        satisfaction_rate = 0

    return {
        'average_feedback_score': round(avg_score, 1),
        'satisfaction_rate': round(satisfaction_rate, 1),
        'total_feedbacks': total_feedbacks
    }

def get_full_dashboard_stats():
    return {
        'complaints': get_complaint_analytics(),
        'performance': get_performance_analytics(),
        'citizens': get_citizen_analytics(),
    }
