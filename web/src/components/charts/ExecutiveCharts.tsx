import React from "react";
import { Card } from "../ui/Card";
import { TrendingUp, BarChart3, PieChart, Activity } from "lucide-react";

export const ExecutiveCharts: React.FC = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-blue-600" /> Resolution Volume by Department
          </h3>
          <span className="text-xs text-slate-500 font-medium">Updated 5 mins ago</span>
        </div>
        <div className="h-64 flex items-end justify-between gap-3 pt-6 border-b border-slate-100 dark:border-slate-800">
          {[
            { label: "Roads", height: "85%", color: "bg-blue-600", val: "482" },
            { label: "Sanitation", height: "92%", color: "bg-emerald-500", val: "614" },
            { label: "Water", height: "65%", color: "bg-cyan-500", val: "320" },
            { label: "Lighting", height: "78%", color: "bg-amber-500", val: "410" },
            { label: "Parks", height: "45%", color: "bg-purple-500", val: "190" },
            { label: "Health", height: "55%", color: "bg-rose-500", val: "245" },
          ].map((bar) => (
            <div key={bar.label} className="flex-1 flex flex-col items-center gap-2">
              <span className="text-xs font-bold text-slate-700 dark:text-slate-300">{bar.val}</span>
              <div className={`w-full rounded-t-lg ${bar.color} transition-all duration-500`} style={{ height: bar.height }} />
              <span className="text-xs text-slate-500 font-medium">{bar.label}</span>
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-emerald-600" /> SLA Compliance Trend (Last 7 Days)
          </h3>
          <span className="text-xs text-emerald-600 font-bold">96.4% City Average</span>
        </div>
        <div className="h-64 flex items-center justify-center bg-slate-50 dark:bg-slate-800/40 rounded-xl p-4">
          <div className="w-full text-center space-y-2">
            <Activity className="h-8 w-8 text-blue-500 mx-auto animate-pulse" />
            <p className="text-xs text-slate-500">Real-time dynamic compliance spline vector rendering</p>
            <div className="flex justify-around text-xs font-semibold text-slate-700 dark:text-slate-300 pt-4">
              <span>Mon: 94.2%</span>
              <span>Tue: 95.8%</span>
              <span>Wed: 96.1%</span>
              <span>Thu: 97.0%</span>
              <span>Fri: 96.4%</span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
