import React from "react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { BarChart3, TrendingUp, Download, Calendar } from "lucide-react";

export const Analytics: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Municipal Performance Analytics</h1>
          <p className="text-sm text-slate-500">Service Level Agreement compliance, ward rankings, and resolution speed benchmarks</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm">
            <Calendar className="h-4 w-4 mr-2" /> Last 30 Days
          </Button>
          <Button variant="primary" size="sm">
            <Download className="h-4 w-4 mr-2" /> Export PDF Summary
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="text-center p-6">
          <p className="text-xs font-semibold text-slate-500 uppercase">Average Resolution Time</p>
          <h2 className="text-3xl font-bold text-blue-600 mt-2">18.4 Hours</h2>
          <p className="text-xs text-emerald-600 font-medium mt-1">↓ 14% improvement month-over-month</p>
        </Card>

        <Card className="text-center p-6">
          <p className="text-xs font-semibold text-slate-500 uppercase">Citizen Satisfaction NPS</p>
          <h2 className="text-3xl font-bold text-emerald-600 mt-2">+68</h2>
          <p className="text-xs text-emerald-600 font-medium mt-1">High Citizen Endorsement</p>
        </Card>

        <Card className="text-center p-6">
          <p className="text-xs font-semibold text-slate-500 uppercase">SLA Compliance Index</p>
          <h2 className="text-3xl font-bold text-purple-600 mt-2">96.2%</h2>
          <p className="text-xs text-slate-500 font-medium mt-1">Target Threshold: 90.0%</p>
        </Card>
      </div>
    </div>
  );
};
