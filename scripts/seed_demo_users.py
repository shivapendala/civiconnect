import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.abspath("backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Municipality, Department, StaffProfile, CitizenProfile, CivicPoints, Badge

User = get_user_model()

def seed():
    print("Seeding demo municipal data & credentials...")
    
    # 1. Municipality
    muni, _ = Municipality.objects.get_or_create(
        name="Metro City Civic Administration",
        defaults={"state": "Metro Province", "country": "India", "contact_email": "admin@city.gov", "contact_phone": "+91 9876543210"}
    )
    
    # 2. Departments
    dept_pw, _ = Department.objects.get_or_create(name="Public Works & Roads", municipality=muni)
    dept_water, _ = Department.objects.get_or_create(name="Water Supply & Drainage", municipality=muni)
    dept_sanitation, _ = Department.objects.get_or_create(name="Sanitation & Solid Waste", municipality=muni)
    
    # 3. Superuser Admin (Username: admin, Email: admin@city.gov, Password: adminpassword / admin123)
    admin_user, created = User.objects.get_or_create(
        email="admin@city.gov",
        defaults={"username": "admin", "first_name": "System", "last_name": "Administrator", "is_staff": True, "is_superuser": True, "is_verified": True}
    )
    admin_user.username = "admin"
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.set_password("admin123")
    admin_user.save()
    print("Admin Superuser created: admin / admin@city.gov (Password: admin123)")

    # 4. Staff User (Username: staff, Email: staff@city.gov, Password: password123)
    staff_user, _ = User.objects.get_or_create(
        email="staff@city.gov",
        defaults={"username": "staff", "first_name": "Alex", "last_name": "Engineer", "is_staff": True, "is_verified": True}
    )
    staff_user.username = "staff"
    staff_user.is_staff = True
    staff_user.set_password("password123")
    staff_user.save()
    StaffProfile.objects.get_or_create(user=staff_user, defaults={"municipality": muni, "department": dept_pw, "designation": "Chief Field Engineer"})
    print("Staff User created: staff / staff@city.gov (Password: password123)")

    # 5. Citizen User (Username: citizen, Email: citizen@example.com, Password: password123)
    citizen_user, _ = User.objects.get_or_create(
        email="citizen@example.com",
        defaults={"username": "citizen", "first_name": "Priya", "last_name": "Sharma", "is_verified": True, "phone_number": "9876543210"}
    )
    citizen_user.username = "citizen"
    citizen_user.set_password("password123")
    citizen_user.save()
    cp, _ = CitizenProfile.objects.get_or_create(user=citizen_user, defaults={"municipality": muni, "address": "742 Evergreen Terrace, Sector 4"})
    CivicPoints.objects.get_or_create(citizen=cp, defaults={"total_points": 240, "level": 3})
    print("Citizen User created: citizen / citizen@example.com (Password: password123)")

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()
