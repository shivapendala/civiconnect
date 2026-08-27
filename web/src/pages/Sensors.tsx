import React, { useState } from "react";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Radio, BatteryCharging, Signal, AlertTriangle } from "lucide-react";

export const Sensors: React.FC = () => {
  const [sensors] = useState([
    { id: "IOT-AQI-01", name: "Downtown Plaza AQI", type: "Air Quality (PM2.5)", value: "32 AQI (Good)", battery: "98%", status: "Online" },
    { id: "IOT-BIN-44", name: "Market St Smart Bin", type: "Waste Level", value: "84% (Warning)", battery: "85%", status: "Online" },
    { id: "IOT-WTR-12", name: "Sector 4 Main Valve", type: "Water Pressure", value: "4.2 Bar (Optimal)", battery: "100%", status: "Online" },
    { id: "IOT-LGT-89", name: "Highway Overpass Pole 12", type: "Streetlight Luminaire", value: "Lamp OK", battery: "Main Power", status: "Online" },
  ]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Smart City IoT Telemetry Fleet</h1>
          <p className="text-sm text-slate-500">Autonomous environmental, waste, and infrastructure sensor telemetry</p>
        </div>
        <Button variant="primary" size="sm">+ Register Sensor</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {sensors.map((s) => (
          <Card key={s.id} className="p-5">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono font-bold text-blue-600">{s.id}</span>
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <h3 className="font-bold text-sm text-slate-900 dark:text-white">{s.name}</h3>
            <p className="text-xs text-slate-500 mb-3">{s.type}</p>
            <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg text-xs mb-3">
              <p className="font-semibold text-slate-700 dark:text-slate-300">Live Reading:</p>
              <p className="text-sm font-bold text-slate-900 dark:text-white mt-0.5">{s.value}</p>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Battery: {s.battery}</span>
              <span>Signal: -68 dBm</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
