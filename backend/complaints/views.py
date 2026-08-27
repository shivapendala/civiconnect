from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Complaint, ComplaintCategory
from .serializers import ComplaintSerializer, ComplaintCategorySerializer, FeedbackSerializer
from .services import assign_complaint, override_assignment, resolve_complaint, verify_complaint, reopen_complaint
from .search import search_complaints
from .analytics import get_full_dashboard_stats
from .reports import generate_csv_report, generate_excel_report, generate_pdf_report
from accounts.audit import log_audit_action

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'citizen_profile'):
            return Complaint.objects.filter(citizen=user.citizen_profile)
        return Complaint.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        # Must be a citizen to create a complaint directly through this endpoint
        if hasattr(user, 'citizen_profile'):
            complaint = serializer.save(citizen=user.citizen_profile)
            log_audit_action(user.id, "Created Complaint", "Complaint", complaint.id, new_value=complaint.title, ip_address=self.request.META.get('REMOTE_ADDR'))
            # Auto-assign
            assign_complaint(complaint.id)
        else:
            raise permissions.PermissionDenied("Only citizens can file complaints.")

    @decorators.action(detail=False, methods=['get'])
    def search(self, request):
        """Global Search Endpoint"""
        user = request.user
        citizen_id = user.citizen_profile.id if hasattr(user, 'citizen_profile') else None
        
        # Extract query params
        results = search_complaints(
            page=request.query_params.get('page', 1),
            per_page=request.query_params.get('per_page', 20),
            citizen_id=citizen_id,
            complaint_id=request.query_params.get('complaint_id'),
            category_name=request.query_params.get('category'),
            status=request.query_params.get('status'),
            priority=request.query_params.get('priority'),
            location_query=request.query_params.get('location'),
        )
        # Serialize the results manually since search_complaints returns model instances
        results['results'] = ComplaintSerializer(results['results'], many=True).data
        return Response(results)

    @decorators.action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Staff marks complaint as resolved"""
        user = request.user
        if not hasattr(user, 'staff_profile'):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        success, msg = resolve_complaint(pk, user.staff_profile.id, request.data.get('summary', ''))
        if success:
            log_audit_action(user.id, "Resolved Complaint", "Complaint", pk, ip_address=request.META.get('REMOTE_ADDR'))
            return Response({"status": msg})
        return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Citizen verifies the resolution"""
        user = request.user
        if not hasattr(user, 'citizen_profile'):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        rating = request.data.get('rating')
        comments = request.data.get('comments', '')
        success, msg = verify_complaint(pk, user.citizen_profile.id, rating, comments)
        
        if success:
            log_audit_action(user.id, "Verified Complaint", "Complaint", pk, ip_address=request.META.get('REMOTE_ADDR'))
            return Response({"status": msg})
        return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """Citizen reopens a resolved complaint"""
        user = request.user
        if not hasattr(user, 'citizen_profile'):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        reason = request.data.get('reason', '')
        success, msg = reopen_complaint(pk, user.citizen_profile.id, reason)
        
        if success:
            log_audit_action(user.id, "Reopened Complaint", "Complaint", pk, ip_address=request.META.get('REMOTE_ADDR'))
            return Response({"status": msg})
        return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(detail=False, methods=['get'])
    def dashboard(self, request):
        if hasattr(request.user, 'citizen_profile'):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        stats = get_full_dashboard_stats()
        return Response(stats)

    @decorators.action(detail=False, methods=['get'])
    def reports(self, request):
        if hasattr(request.user, 'citizen_profile'):
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
        format_type = request.query_params.get('format', 'csv')
        queryset = Complaint.objects.all() # Or filter based on params
        
        if format_type == 'csv':
            data = generate_csv_report(queryset)
            response = HttpResponse(data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response
        elif format_type == 'excel':
            data = generate_excel_report(queryset)
            response = HttpResponse(data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            return response
        elif format_type == 'pdf':
            data = generate_pdf_report(queryset)
            response = HttpResponse(data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            return response
            
        return Response({"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)
