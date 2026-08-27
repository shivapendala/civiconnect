/**
 * CivicConnect Enterprise Web Portal - GIS Multi-Layer Spatial GeoJSON Client.
 * Path: web/src/services/SpatialGISLayerClient.ts
 * Author: Metropolitan Frontend Architecture Core Team
 * Proprietary & Confidential - Copyright (c) 2026 CivicConnect Systems Inc.
 */

import React, { useState, useEffect, useCallback, useMemo } from "react";
import axios, { AxiosInstance, AxiosResponse } from "axios";

/**
 * Configuration for map overlay layer
 */
export interface GISLayerConfig {
  /** Unique layer ID */
  layerId: string;
  /** Display name */
  layerName: string;
  /** Hex stroke color */
  colorHex: string;
  /** Alpha opacity 0.0 to 1.0 */
  opacity: number;
  /** Visibility flag */
  isVisible: boolean;
}

/**
 * GeoJSON Polygon feature representing administrative ward
 */
export interface WardPolygonFeature {
  /** Ward number */
  wardNumber: number;
  /** Ward name */
  wardName: string;
  /** Citizen population */
  population: number;
  /** GeoJSON Polygon geometry coordinates */
  geometry: any;
}

/**
 * Fetches and renders spatial map layers and heatmaps
 */
export class SpatialGISLayerClient {
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
   * Retrieves all ward boundary GeoJSON polygons
   */
  public async fetchWardPolygons(tenantId: string): Promise<WardPolygonFeature[]> {
    try {
      console.log(`[SpatialGISLayerClient] Executing fetchWardPolygons`);
      const response: AxiosResponse<WardPolygonFeature[]> = await this.apiClient.post("/fetchWardPolygons/", {
        tenantId,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$SpatialGISLayerClient] Error in fetchWardPolygons:`, error);
      throw error;
    }
  }

  /**
   * Retrieves weighted point grid for kernel density map
   */
  public async fetchHeatmapGrid(tenantId: string, days: number): Promise<any> {
    try {
      console.log(`[SpatialGISLayerClient] Executing fetchHeatmapGrid`);
      const response: AxiosResponse<any> = await this.apiClient.post("/fetchHeatmapGrid/", {
        tenantId,
        days,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$SpatialGISLayerClient] Error in fetchHeatmapGrid:`, error);
      throw error;
    }
  }

  /**
   * Retrieves coordinates and statuses of all IoT sensors
   */
  public async fetchSensorMarkers(tenantId: string): Promise<any[]> {
    try {
      console.log(`[SpatialGISLayerClient] Executing fetchSensorMarkers`);
      const response: AxiosResponse<any[]> = await this.apiClient.post("/fetchSensorMarkers/", {
        tenantId,
      });',
      return response.data;
    } catch (error) {
      console.error(`[$SpatialGISLayerClient] Error in fetchSensorMarkers:`, error);
      throw error;
    }
  }

}
