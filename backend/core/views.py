from django.http import HttpResponse

def index_view(request):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CivicConnect - Municipal Command & Triage Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
        body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; }
        header { background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid #334155; padding: 1.25rem 2rem; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: flex; align-items: center; gap: 0.5rem; }
        .badge { background: #0284c7; color: white; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.6rem; border-radius: 9999px; }
        main { flex: 1; max-width: 1200px; margin: 0 auto; width: 100%; padding: 3rem 1.5rem; }
        .hero { text-align: center; margin-bottom: 3rem; }
        .hero h1 { font-size: 2.75rem; font-weight: 800; letter-spacing: -0.025em; margin-bottom: 0.75rem; background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.125rem; color: #94a3b8; max-width: 650px; margin: 0 auto; line-height: 1.6; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 3rem; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 1rem; padding: 1.75rem; transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s; position: relative; overflow: hidden; }
        .card:hover { transform: translateY(-4px); border-color: #38bdf8; box-shadow: 0 12px 24px -10px rgba(56, 189, 248, 0.2); }
        .card-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
        .card-icon { width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
        .icon-blue { background: rgba(56, 189, 248, 0.15); color: #38bdf8; }
        .icon-emerald { background: rgba(52, 211, 153, 0.15); color: #34d399; }
        .icon-purple { background: rgba(192, 132, 252, 0.15); color: #c084fc; }
        .card-title { font-size: 1.25rem; font-weight: 700; color: #f8fafc; }
        .card-desc { color: #94a3b8; font-size: 0.875rem; line-height: 1.5; margin-bottom: 1.25rem; }
        
        .creds-box { background: #0f172a; border: 1px solid #334155; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1.25rem; font-size: 0.85rem; font-family: monospace; }
        .creds-row { display: flex; justify-content: space-between; margin-bottom: 0.35rem; }
        .creds-row:last-child { margin-bottom: 0; }
        .creds-label { color: #64748b; }
        .creds-val { color: #38bdf8; font-weight: 600; }
        
        .btn { display: inline-flex; align-items: center; justify-content: center; width: 100%; padding: 0.75rem 1.25rem; border-radius: 0.5rem; font-weight: 600; font-size: 0.875rem; text-decoration: none; transition: background-color 0.2s, opacity 0.2s; cursor: pointer; border: none; }
        .btn-primary { background: #0284c7; color: white; }
        .btn-primary:hover { background: #0369a1; }
        .btn-outline { background: transparent; border: 1px solid #475569; color: #cbd5e1; }
        .btn-outline:hover { background: #334155; color: white; }
        
        footer { text-align: center; padding: 1.5rem; border-top: 1px solid #334155; color: #64748b; font-size: 0.875rem; }
    </style>
</head>
<body>
    <header>
        <div class="logo">
            <span>🏛️ CivicConnect</span>
            <span class="badge">v2.4.0 Active</span>
        </div>
        <div>
            <a href="/admin/" class="btn btn-outline" style="width: auto; padding: 0.4rem 1rem;">Admin Console &rarr;</a>
        </div>
    </header>

    <main>
        <div class="hero">
            <h1>Municipal Management & Citizen Triage</h1>
            <p>Enterprise smart city operations, automated grievance workflows, SLA escalation engine, and GIS incident mapping.</p>
        </div>

        <div class="grid">
            <!-- Card 1: Django Administration -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon icon-blue">🛡️</div>
                    <h2 class="card-title">Django Admin Console</h2>
                </div>
                <p class="card-desc">Full governance over users, departments, municipalities, complaints, audit logs, and gamification rewards.</p>
                <div class="creds-box">
                    <div class="creds-row"><span class="creds-label">Username:</span><span class="creds-val">admin</span></div>
                    <div class="creds-row"><span class="creds-label">Email:</span><span class="creds-val">admin@city.gov</span></div>
                    <div class="creds-row"><span class="creds-label">Password:</span><span class="creds-val">admin123</span></div>
                </div>
                <a href="/admin/" class="btn btn-primary">Open Admin Portal &rarr;</a>
            </div>

            <!-- Card 2: Staff & Field Worker Portal -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon icon-emerald">👷</div>
                    <h2 class="card-title">Staff / Field Worker</h2>
                </div>
                <p class="card-desc">Municipal officer accounts for dispatch management, site investigations, and resolution validations.</p>
                <div class="creds-box">
                    <div class="creds-row"><span class="creds-label">Username:</span><span class="creds-val">staff</span></div>
                    <div class="creds-row"><span class="creds-label">Email:</span><span class="creds-val">staff@city.gov</span></div>
                    <div class="creds-row"><span class="creds-label">Password:</span><span class="creds-val">password123</span></div>
                </div>
                <a href="/admin/" class="btn btn-outline">Staff Sign In &rarr;</a>
            </div>

            <!-- Card 3: Citizen Account -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon icon-purple">📱</div>
                    <h2 class="card-title">Citizen Mobile / Web</h2>
                </div>
                <p class="card-desc">Citizen profile with civic karma points, level badges, and mobile grievance reporting permissions.</p>
                <div class="creds-box">
                    <div class="creds-row"><span class="creds-label">Username:</span><span class="creds-val">citizen</span></div>
                    <div class="creds-row"><span class="creds-label">Email:</span><span class="creds-val">citizen@example.com</span></div>
                    <div class="creds-row"><span class="creds-label">Password:</span><span class="creds-val">password123</span></div>
                </div>
                <a href="/api/v1/complaints/" class="btn btn-outline">API Endpoints &rarr;</a>
            </div>
        </div>

        <div style="background: #1e293b; border: 1px solid #334155; border-radius: 1rem; padding: 1.5rem;">
            <h3 style="margin-bottom: 1rem; color: #f8fafc; font-size: 1.1rem;">⚡ Quick API Health & Endpoints</h3>
            <ul style="list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem;">
                <li><a href="/admin/" style="color: #38bdf8; text-decoration: none; font-family: monospace;">GET /admin/</a> &mdash; Administration Dashboard</li>
                <li><a href="/api/v1/complaints/complaints/" style="color: #38bdf8; text-decoration: none; font-family: monospace;">GET /api/v1/complaints/</a> &mdash; Complaints REST API</li>
                <li><a href="/api/v1/complaints/analytics/" style="color: #38bdf8; text-decoration: none; font-family: monospace;">GET /api/v1/analytics/</a> &mdash; Municipal KPIs</li>
                <li><a href="/api/v1/auth/token/" style="color: #38bdf8; text-decoration: none; font-family: monospace;">POST /api/v1/auth/token/</a> &mdash; JWT Token Generator</li>
            </ul>
        </div>
    </main>

    <footer>
        CivicConnect Enterprise Platform &bull; Running locally on Port 8000
    </footer>
</body>
</html>
"""
    return HttpResponse(html)
