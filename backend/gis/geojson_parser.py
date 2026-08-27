import json
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class GeoJSONParser:
    """Parses and validates standard RFC 7946 GeoJSON FeatureCollections, Polygons, and MultiPolygons."""
    
    @staticmethod
    def validate_polygon_geometry(geometry: Dict[str, Any]) -> bool:
        if not isinstance(geometry, dict):
            return False
        geom_type = geometry.get("type")
        if geom_type not in ("Polygon", "MultiPolygon"):
            return False
        coords = geometry.get("coordinates")
        if not coords or not isinstance(coords, list):
            return False
        return True

    @classmethod
    def extract_polygon_rings(cls, geometry: Dict[str, Any]) -> List[List[Tuple[float, float]]]:
        rings = []
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates", [])
        
        if geom_type == "Polygon":
            for ring in coords:
                poly = [(float(pt[1]), float(pt[0])) for pt in ring if len(pt) >= 2]  # convert (lng, lat) -> (lat, lng)
                rings.append(poly)
        elif geom_type == "MultiPolygon":
            for poly_coords in coords:
                for ring in poly_coords:
                    poly = [(float(pt[1]), float(pt[0])) for pt in ring if len(pt) >= 2]
                    rings.append(poly)
                    
        return rings

    @classmethod
    def calculate_centroid(cls, polygon: List[Tuple[float, float]]) -> Tuple[float, float]:
        if not polygon:
            return (0.0, 0.0)
        avg_lat = sum(p[0] for p in polygon) / len(polygon)
        avg_lng = sum(p[1] for p in polygon) / len(polygon)
        return (round(avg_lat, 6), round(avg_lng, 6))
