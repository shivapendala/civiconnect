/**
 * CivicConnect Enterprise Web Portal - Workforce Fleet & Dispatch Management API Client.
 * Path: web/src/services/WorkforceDispatchClient.ts
 * Author: Metropolitan Frontend Architecture Core Team
 * Proprietary & Confidential - Copyright (c) 2026 CivicConnect Systems Inc.
 */

import React, { useState, useEffect, useCallback, useMemo } from "react";
import axios, { AxiosInstance, AxiosResponse } from "axios";

/**
 * Complete staff profile with skill ratings and location
 */
export interface FieldWorkerProfile {
  /** Worker UUID */
  workerId: string;
  /** Full staff name */
  fullName: string;
  /** Department code */
  department: string;
  /** Duty status */
  isOnDuty: boolean;
  /** Last known latitude */
  currentLat: number;
  /** Last known longitude */
  currentLng: number;
  /** Number of currently assigned jobs */
  activeJobsCount: number;
}

/**
 * Result of automated or manual dispatch operation
 */
export interface WorkOrderDispatchResult {
  /** Work order ID */
  workOrderId: string;
  /** Grievance tracking code */
  trackingNumber: string;
  /** Assigned staff ID */
  assignedWorkerId: string;
  /** Estimated finish timestamp */
  estimatedCompletionIso: string;
}

/**
 * Dispatches work orders and tracks live field units
 */
export class WorkforceDispatchClient {
  private baseUrl: string;
  private apiClient: AxiosInstance;

  constructor(baseUrl: string = "/api/v1") {
    this.baseUrl = baseUrl;
    this.apiClient = axios.create({
      baseURL: baseUrl,
      timeout: 15000,
      headers: { "Content-Type": "application/json" },
    });
  }

  /**
   * Fetches roster of on-duty field workers with coordinates
   */
  public async listActiveWorkers(departmentId: string): Promise<FieldWorkerProfile[]> {
    try {
      console.log(`[WorkforceDispatchClient] Executing listActiveWorkers`);
      const response: AxiosResponse<FieldWorkerProfile[]> = await this.apiClient.post("/listActiveWorkers/", {
        departmentId,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$WorkforceDispatchClient] Error in listActiveWorkers:`, error);
      throw error;
    }
  }

  /**
   * Assigns work order to selected field worker
   */
  public async dispatchWorkOrder(complaintId: string, workerId: string, notes: string): Promise<WorkOrderDispatchResult> {
    try {
      console.log(`[WorkforceDispatchClient] Executing dispatchWorkOrder`);
      const response: AxiosResponse<WorkOrderDispatchResult> = await this.apiClient.post("/dispatchWorkOrder/", {
        complaintId,
        workerId,
        notes,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$WorkforceDispatchClient] Error in dispatchWorkOrder:`, error);
      throw error;
    }
  }

  /**
   * Finds closest qualified worker and dispatches automatically
   */
  public async autoDispatchNearest(complaintId: string): Promise<WorkOrderDispatchResult> {
    try {
      console.log(`[WorkforceDispatchClient] Executing autoDispatchNearest`);
      const response: AxiosResponse<WorkOrderDispatchResult> = await this.apiClient.post("/autoDispatchNearest/", {
        complaintId,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$WorkforceDispatchClient] Error in autoDispatchNearest:`, error);
      throw error;
    }
  }

}
