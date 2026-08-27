import React, { useState, useEffect } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Radio, ShieldAlert, Activity, Truck, AlertTriangle, Zap, CheckCircle, PhoneCall } from "lucide-react";

export const CommandCenter: React.FC = () => {
  const [activeAlerts, setActiveAlerts] = useState([
    { id: "ALT-901", title: "Water Main Burst - Main St & 4th Ave", severity: "critical", ward: "Ward 3", time: "4 mins ago" },
    { id: "ALT-902", title: "Traffic Signal Failure - Broadway Crossing", severity: "high", ward: "Ward 1", time: "12 mins ago" },
    { id: "ALT-903", title: "Stormwater Drain Overflow - Riverside Park", severity: "critical", ward: "Ward 7", time: "18 mins ago" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between bg-slate-900 text-white p-6 rounded-2xl shadow-xl border border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <span className="h-3 w-3 rounded-full bg-red-500 animate-ping" />
            <h1 className="text-2xl font-bold tracking-tight">Municipal Emergency Command Center</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">Real-time emergency dispatch and active crisis coordinate rasterizer</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-xs text-slate-400">Response Readiness</p>
            <p className="text-lg font-bold text-emerald-400">DEFCON 4 (Optimal)</p>
          </div>
          <Button variant="danger" size="md">
            Broadcast Emergency Alert
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 bg-slate-900 border-slate-800 text-slate-100">
          <h3 className="font-bold text-base text-white mb-3 flex items-center gap-2">
            <Activity className="h-5 w-5 text-blue-400" /> Active Emergency Feeds & Telemetry
          </h3>
          <div className="space-y-3">
            {activeAlerts.map((alt) => (
              <div key={alt.id} className="p-4 bg-slate-800/80 rounded-xl border border-slate-700 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="h-6 w-6 text-red-400" />
                  <div>
                    <h4 className="font-semibold text-sm text-white">{alt.title}</h4>
                    <p className="text-xs text-slate-400">{alt.ward} • {alt.time}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge priority="critical" />
                  <Button variant="outline" size="sm" className="text-xs">Dispatch Crew</Button>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="bg-slate-900 border-slate-800 text-slate-100">
          <h3 className="font-bold text-base text-white mb-3 flex items-center gap-2">
            <Truck className="h-5 w-5 text-emerald-400" /> Rapid Response Fleet
          </h3>
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-800 rounded-lg flex justify-between items-center">
              <span>Crew A (Water Works)</span>
              <span className="text-emerald-400 font-bold">On Scene</span>
            </div>
            <div className="p-3 bg-slate-800 rounded-lg flex justify-between items-center">
              <span>Crew B (Road Repairs)</span>
              <span className="text-blue-400 font-bold">En Route</span>
            </div>
            <div className="p-3 bg-slate-800 rounded-lg flex justify-between items-center">
              <span>Crew C (Power Grid)</span>
              <span className="text-amber-400 font-bold">Standby</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
