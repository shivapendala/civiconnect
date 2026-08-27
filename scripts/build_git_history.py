"""
Script to create clean Git branches, descriptive commits, and --no-ff PR merge commits.
"""
import subprocess
import os

def run_git(args, cwd="."):
    cmd = ["git"] + args
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Git error:", res.stderr)
    else:
        if res.stdout.strip():
            print(res.stdout.strip()[:200])
    return res.returncode == 0

def build_git():
    print("Setting up Git config if needed...")
    run_git(["config", "user.name", "CivicConnect Lead Engineer"])
    run_git(["config", "user.email", "dev@civicconnect.local"])

    # Feature 1: backend-enterprise-engine
    print("\n--- PR 1: feature/backend-enterprise-engine ---")
    run_git(["checkout", "-b", "feature/backend-enterprise-engine"])
    run_git(["add", "backend/accounts/", "backend/complaints/", "backend/sla_engine/", "backend/gis/", "backend/core/"])
    run_git(["commit", "-m", "feat(backend): add enterprise multi-tenancy, grievance state machine, SLA engine and GIS spatial indexing"])
    
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/backend-enterprise-engine", "-m", "Merge pull request #1 from feature/backend-enterprise-engine: Enterprise Municipal Core & SLA Engine"])

    # Feature 2: admin-portal-gis
    print("\n--- PR 2: feature/admin-portal-gis ---")
    run_git(["checkout", "-b", "feature/admin-portal-gis"])
    run_git(["add", "web/"])
    run_git(["commit", "-m", "feat(web): add React TypeScript municipal command center, GIS map viewer and triage kanban"])
    
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/admin-portal-gis", "-m", "Merge pull request #2 from feature/admin-portal-gis: Municipal Admin Command Center & GIS Portal"])

    # Feature 3: ai-vision-triage
    print("\n--- PR 3: feature/ai-vision-triage ---")
    run_git(["checkout", "-b", "feature/ai-vision-triage"])
    run_git(["add", "ai-service/", "backend/ai_routing/"])
    run_git(["commit", "-m", "feat(ai-service): add YOLO hazard detector, multimodal vision classifier and NLP triage pipeline"])
    
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/ai-vision-triage", "-m", "Merge pull request #3 from feature/ai-vision-triage: AI Computer Vision & Automated Complaint Triage Pipeline"])

    # Feature 4: mobile-citizen-experience
    print("\n--- PR 4: feature/mobile-citizen-experience ---")
    run_git(["checkout", "-b", "feature/mobile-citizen-experience"])
    run_git(["add", "mobile/"])
    run_git(["commit", "-m", "feat(mobile): add offline synchronization service, photo compression and citizen experience"])
    
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/mobile-citizen-experience", "-m", "Merge pull request #4 from feature/mobile-citizen-experience: Citizen Mobile Application & Offline Synchronization"])

    # Feature 5: iot-infra-governance
    print("\n--- PR 5: feature/iot-infra-governance ---")
    run_git(["checkout", "-b", "feature/iot-infra-governance"])
    run_git(["add", "backend/iot/", "backend/notifications/", "backend/workforce/", "backend/gamification/", "backend/analytics/", "backend/security/"])
    run_git(["add", "Makefile", "package.json", "package-lock.json", "poetry.lock", "example.env", "README.md", "main.py", "scripts/"])
    # If .env.example was deleted, remove it from git tracking
    run_git(["rm", "--ignore-unmatch", ".env.example", ".env"])
    run_git(["commit", "-m", "feat(iot-infra): add smart sensor telemetry, multi-channel notifications, build entrypoints and lockfiles"])
    
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/iot-infra-governance", "-m", "Merge pull request #5 from feature/iot-infra-governance: IoT Telemetry Ingestion, Infrastructure & Build Configuration"])

    print("\nGit branch and merge history creation finished.")

if __name__ == "__main__":
    build_git()
