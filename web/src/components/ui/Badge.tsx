import React from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { ComplaintStatus, PriorityLevel } from "../../types";

export interface BadgeProps {
  status?: ComplaintStatus;
  priority?: PriorityLevel;
  label?: string;
  variant?: "default" | "success" | "warning" | "danger" | "info";
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ status, priority, label, variant, className }) => {
  let text = label || "";
  let colorClass = "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300";

  if (status) {
    text = status.replace("_", " ").toUpperCase();
    switch (status) {
      case "submitted":
        colorClass = "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300";
        break;
      case "triaged":
        colorClass = "bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-300";
        break;
      case "assigned":
      case "in_progress":
        colorClass = "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300";
        break;
      case "resolved":
      case "verified":
        colorClass = "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300";
        break;
      case "escalated":
      case "rejected":
        colorClass = "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border border-rose-300";
        break;
    }
  } else if (priority) {
    text = priority.toUpperCase();
    switch (priority) {
      case "critical":
        colorClass = "bg-red-600 text-white font-bold animate-pulse";
        break;
      case "high":
        colorClass = "bg-orange-500 text-white font-semibold";
        break;
      case "medium":
        colorClass = "bg-blue-500 text-white";
        break;
      case "low":
        colorClass = "bg-slate-500 text-white";
        break;
    }
  }

  return (
    <span
      className={twMerge(
        clsx(
          "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium tracking-wide uppercase",
          colorClass,
          className
        )
      )}
    >
      {text}
    </span>
  );
};
