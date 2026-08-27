import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { complaintService } from "../services/complaintService";
import { Complaint } from "../types";
import { ArrowLeft, Clock, MapPin, User, MessageSquare, AlertCircle, CheckCircle, Shield } from "lucide-react";

export const ComplaintDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [complaint, setComplaint] = useState<Complaint | null>(null);
  const [newComment, setNewComment] = useState("");
  const [isInternal, setIsInternal] = useState(false);

  useEffect(() => {
    if (id) {
      complaintService.getComplaintById(id).then(setComplaint).catch(console.error);
    }
  }, [id]);

  if (!complaint) {
    return <div className="p-8 text-center text-slate-500">Loading grievance investigation dossier...</div>;
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <Link to="/complaints" className="inline-flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 font-medium">
          <ArrowLeft className="h-4 w-4" /> Back to Complaints List
        </Link>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm">Print Work Order</Button>
          <Button variant="primary" size="sm">Dispatch Field Crew</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-sm font-bold text-blue-600">{complaint.tracking_number}</span>
              <div className="flex items-center gap-2">
                <Badge status={complaint.status} />
                <Badge priority={complaint.priority} />
              </div>
            </div>

            <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">{complaint.title}</h1>
            <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed mb-6">{complaint.description}</p>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl text-xs">
              <div>
                <p className="text-slate-400 font-semibold">Category</p>
                <p className="font-bold text-slate-800 dark:text-slate-200 mt-0.5">{complaint.category_name}</p>
              </div>
              <div>
                <p className="text-slate-400 font-semibold">Ward Boundary</p>
                <p className="font-bold text-slate-800 dark:text-slate-200 mt-0.5">{complaint.ward_name}</p>
              </div>
              <div>
                <p className="text-slate-400 font-semibold">Reported Date</p>
                <p className="font-bold text-slate-800 dark:text-slate-200 mt-0.5">{new Date(complaint.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          </Card>

          {/* Activity & Comment Thread */}
          <Card className="p-6">
            <h3 className="font-bold text-base text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-blue-600" /> Resolution Activity & Staff Notes
            </h3>

            <div className="space-y-4 mb-6">
              {complaint.comments?.map((com) => (
                <div key={com.id} className="p-4 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-xs text-slate-900 dark:text-white">{com.author_name}</span>
                    <span className="text-xs text-slate-400">{new Date(com.created_at).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300">{com.content}</p>
                </div>
              ))}
            </div>

            <div className="space-y-3">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add an internal staff note or citizen update..."
                className="w-full p-3 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500"
                rows={3}
              />
              <div className="flex items-center justify-between">
                <label className="flex items-center gap-2 text-xs text-slate-500 cursor-pointer">
                  <input type="checkbox" checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} className="rounded" />
                  Internal Staff Note Only
                </label>
                <Button size="sm" onClick={() => {
                  if (newComment) {
                    complaintService.addComment(complaint.id, newComment, isInternal);
                    setNewComment("");
                  }
                }}>
                  Post Comment
                </Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Sidebar Info */}
        <div className="space-y-6">
          <Card className="p-5">
            <h4 className="font-bold text-sm text-slate-900 dark:text-white mb-3">SLA Compliance Window</h4>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-100 dark:border-slate-800">
                <span className="text-slate-500">First Response SLA:</span>
                <span className="font-semibold text-emerald-600">Met in 1.8 hrs</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100 dark:border-slate-800">
                <span className="text-slate-500">Resolution Deadline:</span>
                <span className="font-semibold text-slate-900 dark:text-white">{complaint.hours_remaining} hrs left</span>
              </div>
            </div>
          </Card>

          <Card className="p-5">
            <h4 className="font-bold text-sm text-slate-900 dark:text-white mb-3">AI Vision Confidence</h4>
            <div className="p-3 bg-blue-50 dark:bg-blue-950/50 rounded-xl text-xs space-y-1">
              <p className="font-semibold text-blue-900 dark:text-blue-200">Neural Detection: Pothole (96.4%)</p>
              <p className="text-slate-500">Hazard Severity Score: 0.82 / 1.0 (Severe)</p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
