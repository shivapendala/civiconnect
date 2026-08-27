import React, { useState, useEffect, useMemo } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Activity, Shield, MapPin, Users, Radio, BarChart3, Download, RefreshCw, AlertTriangle, CheckCircle2, Clock } from "lucide-react";

export const FieldWorkforceFleet: React.FC = () => {
  const [dataList, setDataList] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    const timer = setTimeout(() => {
      setDataList([
        { id: "REC-101", name: "Sector 4 Water Pressure Invariant", category: "Water Infrastructure", status: "Optimal", timestamp: "2 mins ago" },
        { id: "REC-102", name: "Broadway Pothole Rapid Patching", category: "Road Works", status: "In Progress", timestamp: "14 mins ago" },
        { id: "REC-103", name: "Ward 3 Automated Waste Pickup", category: "Sanitation", status: "Completed", timestamp: "32 mins ago" },
        { id: "REC-104", name: "Downtown Luminaire Grid Circuit", category: "Power Lighting", status: "Optimal", timestamp: "45 mins ago" },
        { id: "REC-105", name: "Riverside Drainage Level Gauge", category: "Stormwater", status: "Warning", timestamp: "1 hour ago" },
      ]);
      setIsLoading(false);
    }, 400);
    return () => clearTimeout(timer);
  }, []);

  const filteredItems = useMemo(() => {
    return dataList.filter((item) => item.name.toLowerCase().includes(searchQuery.toLowerCase()) || item.category.toLowerCase().includes(searchQuery.toLowerCase()));
  }, [dataList, searchQuery]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Live Field Crew Fleet Tracking & Shift Management</h1>
          <p className="text-xs text-slate-500 mt-1">Enterprise Operational Suite • Metropolitan CivicConnect v2.4.0</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={() => setIsLoading(true)}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? "animate-spin" : ""}`} /> Refresh Feed
          </Button>
          <Button variant="primary" size="sm">
            <Download className="h-4 w-4 mr-2" /> Export Dossier
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 flex items-center gap-4 border-l-4 border-l-blue-600">
          <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-xl text-blue-600">
            <Activity className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Active Units</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">1,284</h3>
            <p className="text-xs text-emerald-600 font-medium">99.8% Online</p>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4 border-l-4 border-l-emerald-600">
          <div className="p-3 bg-emerald-50 dark:bg-emerald-950 rounded-xl text-emerald-600">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Compliance Index</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">97.4%</h3>
            <p className="text-xs text-emerald-600 font-medium">Within Target</p>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4 border-l-4 border-l-amber-500">
          <div className="p-3 bg-amber-50 dark:bg-amber-950 rounded-xl text-amber-600">
            <Clock className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Avg Resolution</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">14.2h</h3>
            <p className="text-xs text-emerald-600 font-medium">-2.1h vs Last Week</p>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4 border-l-4 border-l-purple-600">
          <div className="p-3 bg-purple-50 dark:bg-purple-950 rounded-xl text-purple-600">
            <Shield className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 uppercase">Security Integrity</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">100%</h3>
            <p className="text-xs text-purple-600 font-medium">Zero Breaches</p>
          </div>
        </Card>
      </div>

      <Card className="p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Search records by name, ID or category..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="px-4 py-2 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white w-72 focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex items-center gap-2 text-xs">
            <button className={`px-3 py-1.5 rounded-lg font-medium ${activeTab === "overview" ? "bg-blue-600 text-white" : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"}`} onClick={() => setActiveTab("overview")}>Overview</button>
            <button className={`px-3 py-1.5 rounded-lg font-medium ${activeTab === "logs" ? "bg-blue-600 text-white" : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"}`} onClick={() => setActiveTab("logs")}>Audit Logs</button>
            <button className={`px-3 py-1.5 rounded-lg font-medium ${activeTab === "settings" ? "bg-blue-600 text-white" : "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"}`} onClick={() => setActiveTab("settings")}>Config</button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Record Identifier</th>
                <th className="px-4 py-3">Title & Classification</th>
                <th className="px-4 py-3">Operational Status</th>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                  <td className="px-4 py-3 font-mono font-bold text-blue-600">{item.id}</td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-slate-900 dark:text-white">{item.name}</p>
                    <p className="text-xs text-slate-500">{item.category}</p>
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300">
                      {item.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-400">{item.timestamp}</td>
                  <td className="px-4 py-3">
                    <Button variant="outline" size="sm" className="text-xs">Inspect Details →</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
export default FieldWorkforceFleet;
