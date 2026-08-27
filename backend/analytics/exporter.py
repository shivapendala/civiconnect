import csv
import io
from django.http import HttpResponse
from django.utils import timezone
from complaints.models import Complaint

class ReportExporter:
    @staticmethod
    def export_complaints_csv(queryset):
        """Streams complaints queryset into a clean CSV download file."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Tracking Number", "Title", "Category", "Department", "Ward",
            "Status", "Priority", "Citizen", "Assigned Worker",
            "Created At", "SLA Resolution Due", "Is Breached"
        ])
        
        for c in queryset.select_related("category", "department", "ward", "citizen", "assigned_worker"):
            writer.writerow([
                c.tracking_number,
                c.title,
                c.category.name if c.category else "N/A",
                c.department.name if c.department else "N/A",
                f"Ward {c.ward.ward_number}" if c.ward else "N/A",
                c.status,
                c.priority,
                c.citizen.email,
                c.assigned_worker.get_full_name() if c.assigned_worker else "Unassigned",
                c.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                c.sla_resolution_due.strftime("%Y-%m-%d %H:%M:%S") if c.sla_resolution_due else "N/A",
                "YES" if c.is_sla_breached else "NO"
            ])
            
        output.seek(0)
        filename = f"complaints_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
