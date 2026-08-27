import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from accounts.models import CitizenProfile, StaffProfile, Department
from complaints.models import Complaint, ComplaintCategory, ComplaintStatus
import json

User = get_user_model()

@pytest.mark.django_db
class TestComplaintEndToEndFlow:
    """
    Test the E2E Flow: 
    Register -> Login -> Report Complaint -> Assign -> Staff Resolves -> Citizen Verifies -> Feedback
    """

    def setup_method(self):
        self.client = APIClient()
        
        # 1. Setup Base Data
        self.department = Department.objects.create(name="Public Works")
        self.category = ComplaintCategory.objects.create(name="Pothole", department=self.department)
        
        # 2. Setup Staff User
        self.staff_user = User.objects.create_user(username="staff", email="staff@city.gov", password="password123")
        self.staff_profile = StaffProfile.objects.create(user=self.staff_user, department=self.department)

        # 3. Setup Admin User (For search/assignment viewing)
        self.admin_user = User.objects.create_superuser(username="admin", email="admin@city.gov", password="adminpassword")

    def test_full_complaint_lifecycle(self):
        # Step 1: Register
        citizen_user = User.objects.create_user(username="citizen", email="citizen@example.com", password="password123", phone_number="1234567890")
        citizen_profile = CitizenProfile.objects.create(user=citizen_user, address="123 Main St")
        
        # Step 2: Login (Get JWT Token)
        res = self.client.post('/api/auth/login/', {'email': 'citizen@example.com', 'password': 'password123'})
        assert res.status_code == 200
        citizen_token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + citizen_token)
        
        # Step 3: Report Complaint
        complaint_data = {
            "title": "Huge Pothole on 5th Ave",
            "description": "It damaged my tire.",
            "category": self.category.id
        }
        res = self.client.post('/api/complaints/', complaint_data)
        assert res.status_code == 201
        complaint_id = res.data['id']
        
        # Check DB for updated status from auto-assignment
        complaint = Complaint.objects.get(id=complaint_id)
        assert complaint.status == ComplaintStatus.ASSIGNED

        # Step 4: Admin Search / View
        admin_res = self.client.post('/api/auth/login/', {'email': 'admin@city.gov', 'password': 'adminpassword'})
        admin_token = admin_res.data['access']
        admin_client = APIClient()
        admin_client.credentials(HTTP_AUTHORIZATION='Bearer ' + admin_token)
        
        search_res = admin_client.get('/api/complaints/search/')
        assert search_res.status_code == 200
        assert search_res.data['total_results'] >= 1
        
        # Step 5: Staff Resolves
        staff_res = self.client.post('/api/auth/login/', {'email': 'staff@city.gov', 'password': 'password123'})
        staff_token = staff_res.data['access']
        staff_client = APIClient()
        staff_client.credentials(HTTP_AUTHORIZATION='Bearer ' + staff_token)
        
        resolve_data = {"summary": "Filled the pothole."}
        resolve_res = staff_client.post(f'/api/complaints/{complaint_id}/resolve/', resolve_data)
        assert resolve_res.status_code == 200
        
        # Step 6: Citizen Verifies and Leaves Feedback
        verify_data = {
            "rating": 5,
            "comments": "Great fast job!"
        }
        verify_res = self.client.post(f'/api/complaints/{complaint_id}/verify/', verify_data)
        assert verify_res.status_code == 200
        
        # Assert Final State
        complaint = Complaint.objects.get(id=complaint_id)
        assert complaint.status == ComplaintStatus.CLOSED
        assert complaint.feedback.rating == 5
        assert complaint.resolution.summary == "Filled the pothole."
