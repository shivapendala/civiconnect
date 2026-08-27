import React, { useState } from "react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Layers, MapPin, Radio, Shield, AlertTriangle } from "lucide-react";

export const GISMap: React.FC = () => {
  const [activeLayers, setActiveLayers] = useState({
    potholes: true,
    waste: true,
    water: true,
    streetlights: true,
    wards: true,
    heatmaps: false,
  });

  const toggleLayer = (key: keyof typeof activeLayers) => {
    setActiveLayers((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="relative h-[calc(100vh-8rem)] w-full rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 shadow-lg">
      {/* Map Layer Controls Floating Panel */}
      <div className="absolute top-4 left-4 z-20 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-md w-72">
        <div className="flex items-center gap-2 mb-3">
          <Layers className="h-5 w-5 text-blue-600" />
          <h3 className="font-semibold text-slate-900 dark:text-white text-sm">GIS Layer Controls</h3>
        </div>

        <div className="space-y-2 text-xs">
          <label className="flex items-center justify-between cursor-pointer">
            <span className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-amber-500" /> Potholes & Roads
            </span>
            <input
              type="checkbox"
              checked={activeLayers.potholes}
              onChange={() => toggleLayer("potholes")}
              className="rounded text-blue-600"
            />
          </label>

          <label className="flex items-center justify-between cursor-pointer">
            <span className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" /> Waste & Sanitation
            </span>
            <input
              type="checkbox"
              checked={activeLayers.waste}
              onChange={() => toggleLayer("waste")}
              className="rounded text-blue-600"
            />
          </label>

          <label className="flex items-center justify-between cursor-pointer">
            <span className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-blue-500" /> Water Supply & Drainage
            </span>
            <input
              type="checkbox"
              checked={activeLayers.water}
              onChange={() => toggleLayer("water")}
              className="rounded text-blue-600"
            />
          </label>

          <label className="flex items-center justify-between cursor-pointer">
            <span className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-purple-500" /> Smart Streetlights
            </span>
            <input
              type="checkbox"
              checked={activeLayers.streetlights}
              onChange={() => toggleLayer("streetlights")}
              className="rounded text-blue-600"
            />
          </label>

          <hr className="my-2 border-slate-200 dark:border-slate-800" />

          <label className="flex items-center justify-between cursor-pointer">
            <span className="font-medium text-slate-700 dark:text-slate-300">Ward Boundaries</span>
            <input
              type="checkbox"
              checked={activeLayers.wards}
              onChange={() => toggleLayer("wards")}
              className="rounded text-blue-600"
            />
          </label>

          <label className="flex items-center justify-between cursor-pointer">
            <span className="font-medium text-slate-700 dark:text-slate-300">Density Heatmap</span>
            <input
              type="checkbox"
              checked={activeLayers.heatmaps}
              onChange={() => toggleLayer("heatmaps")}
              className="rounded text-blue-600"
            />
          </label>
        </div>
      </div>

      {/* Map Canvas Placeholder & Live Marker Simulation */}
      <div className="h-full w-full bg-slate-100 dark:bg-slate-950 flex items-center justify-center relative">
        <div className="text-center">
          <MapPin className="h-12 w-12 text-blue-600 mx-auto animate-bounce mb-2" />
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">Interactive GIS Spatial Engine</h2>
          <p className="text-sm text-slate-500">Live coordinates: 40.7128° N, 74.0060° W | High precision polygon rasterizer</p>
        </div>
      </div>
    </div>
  );
};
