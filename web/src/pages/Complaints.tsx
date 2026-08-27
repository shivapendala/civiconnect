import React, { useState, useEffect } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { complaintService } from "../services/complaintService";
import { Complaint } from "../types";
import { Search, Filter, Download, Plus, ArrowUpDown } from "lucide-react";
import { Link } from "react-router-dom";

export const Complaints: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    complaintService.getComplaints().then((res) => setComplaints(res.results || []));
  }, []);

  const filtered = complaints.filter((c) => {
    const matchesSearch = c.title.toLowerCase().includes(searchTerm.toLowerCase()) || c.tracking_number.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === "all" || c.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Grievance Management Registry</h1>
          <p className="text-sm text-slate-500">Search, filter, assign, and resolve reported municipal grievances</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={() => complaintService.exportCSV()}>
            <Download className="h-4 w-4 mr-2" /> Export
          </Button>
          <Button variant="primary" size="sm">
            <Plus className="h-4 w-4 mr-2" /> Log Incident
          </Button>
        </div>
      </div>

      <Card className="p-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search by tracking number, title, or address..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
          >
            <option value="all">All Statuses</option>
            <option value="submitted">Submitted</option>
            <option value="triaged">Triaged</option>
            <option value="assigned">Assigned</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="escalated">SLA Escalated</option>
          </select>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">Tracking #</th>
                <th className="px-4 py-3">Title & Department</th>
                <th className="px-4 py-3">Ward</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Priority</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {filtered.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                  <td className="px-4 py-3 font-mono font-bold text-blue-600">{c.tracking_number}</td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-slate-900 dark:text-white">{c.title}</p>
                    <p className="text-xs text-slate-500">{c.department_name}</p>
                  </td>
                  <td className="px-4 py-3">{c.ward_name}</td>
                  <td className="px-4 py-3"><Badge status={c.status} /></td>
                  <td className="px-4 py-3"><Badge priority={c.priority} /></td>
                  <td className="px-4 py-3">
                    <Link to={`/complaints/${c.id}`} className="text-xs text-blue-600 font-semibold hover:underline">
                      Investigate →
                    </Link>
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
