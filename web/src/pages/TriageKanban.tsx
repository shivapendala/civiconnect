import React, { useState, useEffect } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Complaint, ComplaintStatus } from "../types";
import { complaintService } from "../services/complaintService";
import { Clock, UserCheck, AlertOctagon, CheckCircle2 } from "lucide-react";

const COLUMNS: { id: ComplaintStatus; title: string; color: string }[] = [
  { id: "submitted", title: "New / Submitted", color: "border-t-blue-500" },
  { id: "triaged", title: "AI Validated", color: "border-t-purple-500" },
  { id: "assigned", title: "Dispatched", color: "border-t-amber-500" },
  { id: "in_progress", title: "In Progress", color: "border-t-indigo-500" },
  { id: "resolved", title: "Resolved & Closed", color: "border-t-emerald-500" },
];

export const TriageKanban: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const res = await complaintService.getComplaints({ limit: 50 });
        setComplaints(res.results || []);
      } catch (err) {
        console.error("Failed to load complaints for kanban", err);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Grievance Triage Kanban</h1>
        <p className="text-sm text-slate-500">Drag and drop or review lifecycle state progression</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 h-[calc(100vh-12rem)] overflow-x-auto">
        {COLUMNS.map((col) => {
          const colItems = complaints.filter((c) => c.status === col.id);
          return (
            <div key={col.id} className="bg-slate-50 dark:bg-slate-900/50 rounded-xl p-3 flex flex-col h-full border border-slate-200 dark:border-slate-800">
              <div className="flex items-center justify-between mb-3 px-1">
                <h3 className="font-bold text-sm text-slate-800 dark:text-slate-200">{col.title}</h3>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                  {colItems.length}
                </span>
              </div>

              <div className="space-y-3 overflow-y-auto flex-1 pr-1">
                {colItems.map((c) => (
                  <Card key={c.id} className={`p-4 border-t-4 ${col.color} hover:shadow-md transition-shadow`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-mono font-bold text-blue-600">{c.tracking_number}</span>
                      <Badge priority={c.priority} />
                    </div>
                    <h4 className="font-semibold text-sm text-slate-900 dark:text-white mb-1 line-clamp-2">{c.title}</h4>
                    <p className="text-xs text-slate-500 mb-3">{c.category_name}</p>
                    <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-100 dark:border-slate-800">
                      <span>{c.ward_name}</span>
                      <span>{c.hours_remaining}h left</span>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
