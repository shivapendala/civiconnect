import React from "react";
import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { GISMap } from "./pages/GISMap";
import { TriageKanban } from "./pages/TriageKanban";
import { LayoutDashboard, Map, Kanboan as KanbanIcon, ListTodo, Radio, BarChart3, Settings, Shield } from "lucide-react";

const Navigation: React.FC = () => {
  const location = useLocation();
  const navItems = [
    { to: "/", label: "Dashboard", icon: LayoutDashboard },
    { to: "/gis", label: "GIS Command Map", icon: Map },
    { to: "/kanban", label: "Triage Kanban", icon: ListTodo },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col justify-between p-4 border-r border-slate-800">
      <div>
        <div className="flex items-center gap-3 px-3 py-4 mb-6">
          <div className="h-9 w-9 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
            CC
          </div>
          <div>
            <h2 className="font-bold text-white tracking-wide">CivicConnect</h2>
            <p className="text-xs text-slate-400">Municipal Platform</p>
          </div>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = location.pathname === item.to;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  active ? "bg-blue-600 text-white shadow-sm" : "hover:bg-slate-800 hover:text-white"
                }`}
              >
                <Icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-3 bg-slate-800/60 rounded-xl text-xs text-slate-400">
        <p className="font-semibold text-slate-200 mb-1">Enterprise Edition</p>
        <p>Tenant: Metropolitan City Council</p>
      </div>
    </aside>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-100 dark:bg-slate-950 font-sans antialiased text-slate-900 dark:text-slate-100">
        <Navigation />
        <main className="flex-1 overflow-y-auto p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/gis" element={<GISMap />} />
            <Route path="/kanban" element={<TriageKanban />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
