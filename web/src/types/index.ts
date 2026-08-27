export type UserRole = 
  | "citizen"
  | "field_worker"
  | "triage_officer"
  | "ward_officer"
  | "dept_manager"
  | "municipal_admin"
  | "super_admin";

export type ComplaintStatus = 
  | "submitted"
  | "triaged"
  | "assigned"
  | "in_progress"
  | "resolved"
  | "verified"
  | "rejected"
  | "duplicate"
  | "escalated";

export type PriorityLevel = "low" | "medium" | "high" | "critical";

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  role: UserRole;
  tenant?: string;
  tenant_name?: string;
  department?: string;
  department_name?: string;
  assigned_ward?: string;
  ward_name?: string;
  avatar?: string;
  badge_title: string;
  karma_points: number;
  reports_submitted: number;
  reports_resolved: number;
}

export interface ComplaintCategory {
  id: string;
  tenant: string;
  department: string;
  department_name: string;
  name: string;
  code: string;
  description: string;
  icon_name: string;
  color_code: string;
  default_priority: PriorityLevel;
  sla_resolution_hours: number;
  sla_response_hours: number;
  requires_photo: boolean;
  is_active: boolean;
}

export interface ComplaintAttachment {
  id: string;
  file: string;
  file_type: "image" | "video" | "audio" | "document";
  uploader: string;
  uploader_name: string;
  is_resolution_proof: boolean;
  ai_analyzed: boolean;
  ai_labels: string[];
  created_at: string;
}

export interface ComplaintComment {
  id: string;
  complaint: string;
  author: string;
  author_name: string;
  author_role: string;
  content: string;
  is_internal_staff_note: boolean;
  created_at: string;
}

export interface Complaint {
  id: string;
  tracking_number: string;
  tenant: string;
  department?: string;
  department_name?: string;
  ward?: string;
  ward_name?: string;
  category?: string;
  category_name?: string;
  citizen: string;
  citizen_name: string;
  assigned_worker?: string;
  assigned_worker_name?: string;
  title: string;
  description: string;
  status: ComplaintStatus;
  priority: PriorityLevel;
  intake_channel: string;
  latitude: number;
  longitude: number;
  address_text: string;
  landmark?: string;
  pincode?: string;
  sla_response_due?: string;
  sla_resolution_due?: string;
  is_sla_breached: boolean;
  hours_remaining: number;
  ai_confidence_score: number;
  ai_severity_score: number;
  upvotes_count: number;
  comments_count: number;
  attachments?: ComplaintAttachment[];
  comments?: ComplaintComment[];
  created_at: string;
  updated_at: string;
}

export interface Ward {
  id: string;
  tenant: string;
  ward_number: number;
  name: string;
  zone_name: string;
  councillor_name: string;
  councillor_email: string;
  councillor_phone: string;
  population: number;
  area_sq_km: number;
  center_latitude?: number;
  center_longitude?: number;
  boundary_geojson?: any;
  is_active: boolean;
}

export interface FieldWorker {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  department_name: string;
  current_latitude?: number;
  current_longitude?: number;
  is_on_duty: boolean;
  active_jobs_count: number;
  reports_resolved: number;
}

export interface SensorDevice {
  id: string;
  device_id: string;
  tenant: string;
  ward_name?: string;
  department_name?: string;
  sensor_type: "air_quality" | "waste_bin" | "water_pressure" | "streetlight";
  name: string;
  latitude: number;
  longitude: number;
  battery_level: number;
  signal_rssi: number;
  is_online: boolean;
  threshold_warning: number;
  threshold_critical: number;
  last_telemetry_at?: string;
}

export interface ExecutiveKPIs {
  timeframe_days: number;
  total_reported: number;
  total_resolved: number;
  total_breached: number;
  sla_compliance_rate: number;
  resolution_rate: number;
  ward_distribution: { ward__ward_number: number; ward__name: string; count: number }[];
  department_distribution: { department__name: string; count: number }[];
}
