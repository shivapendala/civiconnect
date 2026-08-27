import { apiClient } from "./api";
import { Complaint, ComplaintCategory, ComplaintComment } from "../types";

export const complaintService = {
  async getComplaints(params?: Record<string, any>): Promise<{ count: number; results: Complaint[] }> {
    const response = await apiClient.get("/complaints/", { params });
    return response.data;
  },

  async getComplaintById(id: string): Promise<Complaint> {
    const response = await apiClient.get(`/complaints/${id}/`);
    return response.data;
  },

  async transitionStatus(id: string, status: string, reason?: string): Promise<Complaint> {
    const response = await apiClient.post(`/complaints/${id}/transition/`, { status, reason });
    return response.data;
  },

  async addComment(id: string, content: string, isInternal: boolean = false): Promise<ComplaintComment> {
    const response = await apiClient.post(`/complaints/${id}/add_comment/`, { content, is_internal: isInternal });
    return response.data;
  },

  async getCategories(): Promise<ComplaintCategory[]> {
    const response = await apiClient.get("/complaints/categories/");
    return response.data.results || response.data;
  },

  async exportCSV(): Promise<Blob> {
    const response = await apiClient.get("/analytics/export-csv/", { responseType: "blob" });
    return response.data;
  }
};
