import React, { useState } from "react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Clock, Shield, Plus, Edit2, AlertCircle } from "lucide-react";

export const SLAConfig: React.FC = () => {
  const [policies] = useState([
    { id: "1", dept: "Roads & Transportation", priority: "Critical (P1)", response: "2 Hours", resolution: "12 Hours", autoEscalate: true },
    { id: "2", dept: "Roads & Transportation", priority: "High (P2)", response: "4 Hours", resolution: "24 Hours", autoEscalate: true },
    { id: "3", dept: "Waste & Sanitation", priority: "High (P2)", response: "2 Hours", resolution: "8 Hours", autoEscalate: true },
    { id: "4", dept: "Water Supply", priority: "Critical (P1)", response: "1 Hour", resolution: "6 Hours", autoEscalate: true },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">SLA Matrix & Escalation Policies</h1>
          <p className="text-sm text-slate-500">Configure response windows, holiday calendars, and auto-escalation tiers</p>
        </div>
        <Button variant="primary" size="sm"><Plus className="h-4 w-4 mr-2" /> Add Policy</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {policies.map((p) => (
          <Card key={p.id} className="p-5 border-l-4 border-l-blue-600">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-base text-slate-900 dark:text-white">{p.dept}</h3>
              <span className="text-xs font-bold px-2 py-0.5 bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 rounded">
                {p.priority}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-4 py-3 my-2 bg-slate-50 dark:bg-slate-800 rounded-lg text-xs px-3">
              <div>
                <p className="text-slate-400">First Response Window</p>
                <p className="font-bold text-slate-800 dark:text-slate-200 mt-0.5">{p.response}</p>
              </div>
              <div>
                <p className="text-slate-400">Total Resolution Window</p>
                <p className="font-bold text-slate-800 dark:text-slate-200 mt-0.5">{p.resolution}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
