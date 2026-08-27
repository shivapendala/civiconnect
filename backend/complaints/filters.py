import django_filters
from .models import Complaint

class ComplaintFilter(django_filters.FilterSet):
    min_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    max_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    has_photo = django_filters.BooleanFilter(method="filter_has_photo")
    is_breached = django_filters.BooleanFilter(field_name="is_sla_breached")
    category = django_filters.UUIDFilter(field_name="category__id")
    department = django_filters.UUIDFilter(field_name="department__id")
    ward = django_filters.UUIDFilter(field_name="ward__id")
    
    class Meta:
        model = Complaint
        fields = ["status", "priority", "intake_channel", "ward", "department", "category", "is_sla_breached"]

    def filter_has_photo(self, queryset, name, value):
        if value:
            return queryset.filter(attachments__file_type="image").distinct()
        return queryset
