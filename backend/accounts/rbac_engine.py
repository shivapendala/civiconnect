import logging
from typing import Set, Dict, List, Optional
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

class RolePermissionsEngine:
    """
    Granular Role-Based Access Control (RBAC) engine defining hierarchical permissions
    for citizen reporting, field workforce triage, department dispatch, and municipal oversight.
    """
    PERMISSIONS_MATRIX: Dict[str, Set[str]] = {
        "citizen": {
            "complaint:create",
            "complaint:view_public",
            "complaint:view_own",
            "complaint:vote",
            "complaint:comment",
            "profile:edit_own",
            "gamification:view_leaderboard",
        },
        "field_worker": {
            "complaint:view_assigned",
            "complaint:view_ward",
            "complaint:update_status",
            "complaint:upload_resolution_proof",
            "complaint:internal_comment",
            "workforce:view_own_orders",
            "workforce:update_location",
            "workforce:complete_job",
        },
        "triage_officer": {
            "complaint:view_all_tenant",
            "complaint:triage",
            "complaint:assign_worker",
            "complaint:assign_team",
            "complaint:change_priority",
            "complaint:mark_duplicate",
            "complaint:reject",
            "ai:run_triage",
            "ai:verify_duplicates",
            "workforce:view_fleet",
        },
        "ward_officer": {
            "complaint:view_ward",
            "complaint:escalate",
            "complaint:endorse_priority",
            "gis:view_ward_map",
            "analytics:view_ward_kpis",
            "workforce:view_ward_teams",
        },
        "dept_manager": {
            "complaint:view_department",
            "complaint:reassign",
            "complaint:approve_resolution",
            "sla:configure_department_policies",
            "sla:view_breaches",
            "workforce:manage_department_teams",
            "analytics:view_department_reports",
            "analytics:export_data",
        },
        "municipal_admin": {
            "tenant:view_settings",
            "tenant:manage_departments",
            "tenant:manage_wards",
            "users:manage_staff",
            "sla:configure_global_policies",
            "analytics:view_executive_dashboard",
            "audit:view_logs",
            "iot:manage_sensors",
            "security:view_reports",
        },
        "super_admin": {
            "*",  # All privileges
        }
    }

    @classmethod
    def get_role_permissions(cls, role: str) -> Set[str]:
        return cls.PERMISSIONS_MATRIX.get(role, set())

    @classmethod
    def has_permission(cls, user: User, required_permission: str) -> bool:
        if not user.is_authenticated or not user.is_active:
            return False
            
        if user.role == "super_admin" or user.is_superuser:
            return True
            
        perms = cls.get_role_permissions(user.role)
        if "*" in perms or required_permission in perms:
            return True
            
        # Check wildcard matching e.g. "complaint:*"
        resource = required_permission.split(":")[0]
        if f"{resource}:*" in perms:
            return True
            
        return False
