"""
CivicConnect - Unified Management Entrypoint & Microservices CLI.
Proprietary & Confidential - Metropolitan Smart City Solutions.
"""
import sys
import os
import argparse
import subprocess

def run_backend():
    print("Starting CivicConnect Enterprise Backend (Django/Channels)...")
    cmd = [sys.executable, "backend/manage.py", "runserver", "0.0.0.0:8000"]
    subprocess.run(cmd)

def run_ai_service():
    print("Starting CivicConnect AI & Computer Vision Service...")
    cmd = [sys.executable, "-m", "uvicorn", "ai-service.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
    subprocess.run(cmd)

def run_web():
    print("Starting CivicConnect Municipal Web Portal...")
    subprocess.run(["npm", "run", "dev"], cwd="web")

def run_all():
    print("==================================================")
    print("   CivicConnect Smart City & Municipal Platform   ")
    print("==================================================")
    print("Services available:")
    print(" - Backend API & SLA Engine: http://localhost:8000")
    print(" - AI Vision & Triage Microservice: http://localhost:8001")
    print(" - Municipal Admin Command Center: http://localhost:3000")
    print("Use docker-compose up to start all multi-container services.")

def main():
    parser = argparse.ArgumentParser(description="CivicConnect Enterprise Platform Runner")
    parser.add_argument("service", nargs="?", default="all", choices=["all", "backend", "ai", "web", "worker"])
    args = parser.parse_args()

    if args.service == "backend":
        run_backend()
    elif args.service == "ai":
        run_ai_service()
    elif args.service == "web":
        run_web()
    else:
        run_all()

if __name__ == "__main__":
    main()
