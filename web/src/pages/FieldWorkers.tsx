import React, { useState } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Users, Phone, MapPin, CheckCircle, Clock } from "lucide-react";

export const FieldWorkers: React.FC = () => {
  const [workers] = useState([
    { id: "FW-101", name: "David Miller", department: "Roads & Public Works", ward: "Ward 4", phone: "+1 555-0192", status: "Active On Site", jobs: 3 },
    { id: "FW-102", name: "Sarah Jenkins", department: "Sanitation & Waste", ward: "Ward 2", phone: "+1 555-0143", status: "En Route", jobs: 2 },
    { id: "FW-103", name: "Carlos Ramirez", department: "Water Supply", ward: "Ward 6", phone: "+1 555-0188", status: "Available", jobs: 0 },
    { id: "FW-104", name: "Emily Watson", department: "Power & Streetlights", ward: "Ward 1", phone: "+1 555-0177", status: "Active On Site", jobs: 4 },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Field Operations Workforce</h1>
          <p className="text-sm text-slate-500">Live GPS tracking and shift assignments for field crews</p>
        </div>
        <Button variant="primary" size="sm">+ Onboard Worker</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {workers.map((w) => (
          <Card key={w.id} className="p-5 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-mono font-bold text-slate-400">{w.id}</span>
              <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                {w.status}
              </span>
            </div>
            <h3 className="font-bold text-slate-900 dark:text-white text-base">{w.name}</h3>
            <p className="text-xs text-slate-500 mb-3">{w.department}</p>
            <div className="space-y-1.5 text-xs text-slate-600 dark:text-slate-400 border-t pt-3 border-slate-100 dark:border-slate-800">
              <p className="flex items-center gap-2"><MapPin className="h-3.5 w-3.5 text-slate-400" /> {w.ward}</p>
              <p className="flex items-center gap-2"><Phone className="h-3.5 w-3.5 text-slate-400" /> {w.phone}</p>
              <p className="flex items-center gap-2"><Clock className="h-3.5 w-3.5 text-slate-400" /> {w.jobs} Active Work Orders</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
