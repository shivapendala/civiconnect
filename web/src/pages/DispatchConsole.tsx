import React, { useState } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Navigation, Users, MapPin, Truck, AlertTriangle, Send } from "lucide-react";

export const DispatchConsole: React.FC = () => {
  const [unassignedJobs] = useState([
    { id: "INC-881", title: "Severe Pothole on 5th Ave", ward: "Ward 2", priority: "critical", elapsed: "22 mins" },
    { id: "INC-882", title: "Garbage Overflow at Metro Station", ward: "Ward 4", priority: "high", elapsed: "45 mins" },
    { id: "INC-883", title: "Water Pipe Leak near Hospital", ward: "Ward 1", priority: "critical", elapsed: "12 mins" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Smart Automated Dispatch Console</h1>
          <p className="text-sm text-slate-500">Skill-based matching and nearest field crew routing</p>
        </div>
        <Button variant="primary" size="sm">Auto-Dispatch All Pending</Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white">Unassigned Priority Grievances</h3>
          {unassignedJobs.map((job) => (
            <Card key={job.id} className="p-4 flex items-center justify-between hover:shadow-md transition-shadow">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-blue-600">{job.id}</span>
                  <Badge priority={job.priority as any} />
                  <span className="text-xs text-slate-400">Waiting {job.elapsed}</span>
                </div>
                <h4 className="font-semibold text-sm text-slate-900 dark:text-white">{job.title}</h4>
                <p className="text-xs text-slate-500 flex items-center gap-1"><MapPin className="h-3 w-3" /> {job.ward}</p>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">View on Map</Button>
                <Button variant="primary" size="sm"><Send className="h-3.5 w-3.5 mr-1" /> Dispatch Crew</Button>
              </div>
            </Card>
          ))}
        </div>

        <Card className="p-5">
          <h3 className="font-bold text-sm text-slate-900 dark:text-white mb-3 flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-600" /> Available Field Units
          </h3>
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-bold text-slate-900 dark:text-white">Crew Alpha (Roads)</p>
                <p className="text-slate-500">Ward 2 • 0.8 km away</p>
              </div>
              <span className="text-emerald-600 font-bold">Ready</span>
            </div>
            <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg flex justify-between items-center">
              <div>
                <p className="font-bold text-slate-900 dark:text-white">Crew Bravo (Water)</p>
                <p className="text-slate-500">Ward 1 • 1.4 km away</p>
              </div>
              <span className="text-emerald-600 font-bold">Ready</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
