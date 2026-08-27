import math
from typing import List, Tuple, Dict, Optional

class GeofenceEngine:
    """High-performance spatial geofencing and polygon bounding box intersection engine."""
    
    @staticmethod
    def calculate_bounding_box(polygon: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
        min_lat = min(p[0] for p in polygon)
        max_lat = max(p[0] for p in polygon)
        min_lng = min(p[1] for p in polygon)
        max_lng = max(p[1] for p in polygon)
        return (min_lat, min_lng, max_lat, max_lng)

    @classmethod
    def point_in_bounding_box(cls, point: Tuple[float, float], bbox: Tuple[float, float, float, float]) -> bool:
        lat, lng = point
        min_lat, min_lng, max_lat, max_lng = bbox
        return (min_lat <= lat <= max_lat) and (min_lng <= lng <= max_lng)

    @classmethod
    def calculate_polygon_area_sq_km(cls, polygon: List[Tuple[float, float]]) -> float:
        """Calculates spherical polygon surface area in square kilometers."""
        if len(polygon) < 3:
            return 0.0
        r = 6371.0  # Earth radius km
        area = 0.0
        n = len(polygon)
        for i in range(n):
            j = (i + 1) % n
            lat1, lon1 = math.radians(polygon[i][0]), math.radians(polygon[i][1])
            lat2, lon2 = math.radians(polygon[j][0]), math.radians(polygon[j][1])
            area += (lon2 - lon1) * (2 + math.sin(lat1) + math.sin(lat2))
        area = abs(area * r * r / 2.0)
        return round(area, 3)
