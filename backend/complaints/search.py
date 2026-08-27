from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Complaint

def search_complaints(
    page=1,
    per_page=20,
    citizen_id=None,
    complaint_id=None,
    category_name=None,
    status=None,
    priority=None,
    department_name=None,
    date_start=None,
    date_end=None,
    location_query=None,
    staff_id=None
):
    """
    Global search engine for complaints.
    - If citizen_id is provided, strictly filters to that citizen's complaints.
    - Otherwise, acts as an Admin global search.
    - Supports pagination.
    """
    queryset = Complaint.objects.all().order_by('-created_at')

    # Security: Citizen Isolation
    if citizen_id:
        queryset = queryset.filter(citizen_id=citizen_id)

    # Filters
    if complaint_id:
        # Assuming ID format like CC-2026-001 corresponds to DB ID or we just search the DB ID directly
        # If we had a specific char field for complaint number, we would query that.
        queryset = queryset.filter(id=complaint_id)
        
    if category_name:
        queryset = queryset.filter(category__name__icontains=category_name)
        
    if status:
        queryset = queryset.filter(status=status)
        
    if priority:
        queryset = queryset.filter(priority=priority)
        
    if department_name:
        queryset = queryset.filter(category__department__name__icontains=department_name)
        
    if date_start:
        queryset = queryset.filter(created_at__gte=date_start)
        
    if date_end:
        queryset = queryset.filter(created_at__lte=date_end)
        
    if staff_id:
        # Filter by assignments containing this staff member
        queryset = queryset.filter(complaintassignment__staff_id=staff_id)
        
    if location_query:
        # If we had a text address field, we'd search it. 
        # Alternatively, we search description since users often put location there.
        queryset = queryset.filter(
            Q(description__icontains=location_query) | 
            Q(title__icontains=location_query)
        )

    # Distinct is needed because of joins (e.g. assignments)
    queryset = queryset.distinct()

    # Pagination
    paginator = Paginator(queryset, per_page)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return {
        'total_results': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': results.number,
        'has_next': results.has_next(),
        'has_previous': results.has_previous(),
        'results': list(results)
    }
