import React, { useEffect, useState } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { complaintService } from "../services/complaintService";
import { Complaint, ExecutiveKPIs } from "../types";
import { AlertCircle, CheckCircle2, Clock, MapPin, TrendingUp, Users, ShieldAlert, ArrowUpRight } from "lucide-react";

export const Dashboard: React.FC = () => {
  const [recentComplaints, setRecentComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await complaintService.getComplaints({ limit: 6 });
        setRecentComplaints(res.results || []);
      } catch (err) {
        console.error("Failed to load dashboard data", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Header & Quick Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Municipal Command Dashboard</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Live operational overview across all administrative wards</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={() => complaintService.exportCSV()}>
            Export CSV Report
          </Button>
          <Button variant="primary" size="sm">
            + Log Incident
          </Button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="flex items-center gap-4 border-l-4 border-l-blue-600">
          <div className="p-3 bg-blue-50 dark:bg-blue-950 rounded-lg text-blue-600">
            <AlertCircle className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Active Reports</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">1,482</h3>
            <p className="text-xs text-emerald-600 flex items-center gap-1 font-medium mt-1">
              <TrendingUp className="h-3 w-3" /> +12% this week
            </p>
          </div>
        </Card>

        <Card className="flex items-center gap-4 border-l-4 border-l-emerald-600">
          <div className="p-3 bg-emerald-50 dark:bg-emerald-950 rounded-lg text-emerald-600">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Resolution Rate</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">94.8%</h3>
            <p className="text-xs text-emerald-600 font-medium mt-1">Target: 92.0%</p>
          </div>
        </Card>

        <Card className="flex items-center gap-4 border-l-4 border-l-amber-500">
          <div className="p-3 bg-amber-50 dark:bg-amber-950 rounded-lg text-amber-600">
            <Clock className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Avg Response SLA</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">3.2 hrs</h3>
            <p className="text-xs text-slate-500 font-medium mt-1">Under 4.0h limit</p>
          </div>
        </Card>

        <Card className="flex items-center gap-4 border-l-4 border-l-purple-600">
          <div className="p-3 bg-purple-50 dark:bg-purple-950 rounded-lg text-purple-600">
            <Users className="h-6 w-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Active Field Crews</p>
            <h3 className="text-2xl font-bold text-slate-900 dark:text-white">128</h3>
            <p className="text-xs text-slate-500 font-medium mt-1">14 on emergency duty</p>
          </div>
        </Card>
      </div>

      {/* Recent Incident Feed Table */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">Live Incident Feed</h2>
          <a href="/complaints" className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1">
            View All <ArrowUpRight className="h-4 w-4" />
          </a>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Tracking #</th>
                <th className="px-4 py-3">Title & Category</th>
                <th className="px-4 py-3">Ward</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">SLA Window</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {recentComplaints.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                  <td className="px-4 py-3 font-mono font-bold text-blue-600">{c.tracking_number}</td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-slate-900 dark:text-white">{c.title}</p>
                    <p className="text-xs text-slate-500">{c.category_name || "General Issue"}</p>
                  </td>
                  <td className="px-4 py-3">{c.ward_name || "Central"}</td>
                  <td className="px-4 py-3">
                    <Badge status={c.status} />
                  </td>
                  <td className="px-4 py-3">
                    <Badge priority={c.priority} />
                  </td>
                  <td className="px-4 py-3 text-xs">
                    {c.hours_remaining > 0 ? (
                      <span className="text-emerald-600 font-medium">{c.hours_remaining} hrs left</span>
                    ) : (
                      <span className="text-rose-600 font-bold">Breached</span>
                    )}
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
