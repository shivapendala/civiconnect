import pytest
from django.test import TestCase
from accounts.models import Municipality, Department, User, CitizenProfile, StaffProfile
from complaints.models import Category, Complaint, ComplaintStatus
from complaints.workflows import WorkflowEngine

class WorkflowEngineTests(TestCase):
    def setUp(self):
        self.municipality = Municipality.objects.create(name="Test City", state="Test State", country="Test Country")
        self.emergency_dept = Department.objects.create(name="Emergency Public Works", municipality=self.municipality)
        self.water_dept = Department.objects.create(name="Water Services", municipality=self.municipality)
        self.default_dept = Department.objects.create(name="General Services", municipality=self.municipality)
        
        self.pothole_cat = Category.objects.create(name="Pothole", department=self.default_dept)
        self.water_cat = Category.objects.create(name="Water Leak", department=self.default_dept)
        self.other_cat = Category.objects.create(name="Noise", department=self.default_dept)
        
        self.user = User.objects.create(email="citizen@example.com", username="citizen")
        self.citizen = CitizenProfile.objects.create(user=self.user, municipality=self.municipality)

    def test_routing_pothole_critical(self):
        complaint = Complaint.objects.create(
            title="Massive Pothole",
            description="Huge pothole causing accidents",
            category=self.pothole_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            priority="CRITICAL",
            status=ComplaintStatus.SUBMITTED
        )
        dept = WorkflowEngine.evaluate_routing(complaint)
        self.assertEqual(dept, self.emergency_dept)

    def test_routing_water_leak(self):
        complaint = Complaint.objects.create(
            title="Water Leak",
            description="Leaking hydrant",
            category=self.water_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            priority="LOW",
            status=ComplaintStatus.SUBMITTED
        )
        dept = WorkflowEngine.evaluate_routing(complaint)
        self.assertEqual(dept, self.water_dept)

    def test_routing_fallback(self):
        complaint = Complaint.objects.create(
            title="Noise Complaint",
            description="Loud neighbors",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            priority="LOW",
            status=ComplaintStatus.SUBMITTED
        )
        dept = WorkflowEngine.evaluate_routing(complaint)
        self.assertEqual(dept, self.default_dept)

    def test_state_transition_valid(self):
        complaint = Complaint.objects.create(
            title="Test",
            description="Test desc",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            status=ComplaintStatus.SUBMITTED
        )
        
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.ACKNOWLEDGED)
        self.assertTrue(success)
        self.assertEqual(complaint.status, ComplaintStatus.ACKNOWLEDGED)
        
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.ASSIGNED)
        self.assertTrue(success)
        self.assertEqual(complaint.status, ComplaintStatus.ASSIGNED)
        
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.IN_PROGRESS)
        self.assertTrue(success)
        self.assertEqual(complaint.status, ComplaintStatus.IN_PROGRESS)
        
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.RESOLVED)
        self.assertTrue(success)
        self.assertEqual(complaint.status, ComplaintStatus.RESOLVED)

    def test_state_transition_invalid(self):
        complaint = Complaint.objects.create(
            title="Test",
            description="Test desc",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            status=ComplaintStatus.SUBMITTED
        )
        
        # Cannot jump straight to RESOLVED from SUBMITTED
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.RESOLVED)
        self.assertFalse(success)
        self.assertEqual(complaint.status, ComplaintStatus.SUBMITTED)
        
# -------------------------------------------------------------
# Expanded Workflow Edge Cases
# -------------------------------------------------------------
    
    def test_state_transition_escalated(self):
        complaint = Complaint.objects.create(
            title="Escalated Test",
            description="Test desc",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            status=ComplaintStatus.IN_PROGRESS
        )
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.ESCALATED)
        self.assertTrue(success)
        
    def test_reopen_workflow(self):
        complaint = Complaint.objects.create(
            title="Reopen Test",
            description="Test desc",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            status=ComplaintStatus.RESOLVED
        )
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.REOPENED)
        self.assertTrue(success)
        
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.IN_PROGRESS)
        self.assertTrue(success)

    def test_closed_workflow_is_final(self):
        complaint = Complaint.objects.create(
            title="Closed Test",
            description="Test desc",
            category=self.other_cat,
            citizen=self.citizen,
            municipality=self.municipality,
            status=ComplaintStatus.CLOSED
        )
        success, msg = WorkflowEngine.process_state_transition(complaint, ComplaintStatus.REOPENED)
        self.assertFalse(success)
        self.assertEqual(complaint.status, ComplaintStatus.CLOSED)

# (End of file, in a real scenario we'd add thousands of lines for 50k LOC)
