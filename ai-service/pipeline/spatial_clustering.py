import math
from typing import List, Dict, Tuple

class DBSCANClusterer:
    """Density-Based Spatial Clustering of Applications with Noise (DBSCAN) for civic incident hotspot discovery."""
    
    def __init__(self, eps_meters: float = 200.0, min_samples: int = 3):
        self.eps_meters = eps_meters
        self.min_samples = min_samples

    def _distance_m(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        lat1, lon1 = p1
        lat2, lon2 = p2
        dlat = (lat2 - lat1) * 111000.0
        dlon = (lon2 - lon1) * 111000.0 * math.cos(math.radians(lat1))
        return math.sqrt(dlat ** 2 + dlon ** 2)

    def fit(self, points: List[Tuple[float, float]]) -> List[int]:
        n = len(points)
        labels = [-1] * n
        cluster_id = 0
        
        for i in range(n):
            if labels[i] != -1:
                continue
            neighbors = [j for j in range(n) if self._distance_m(points[i], points[j]) <= self.eps_meters]
            if len(neighbors) < self.min_samples:
                labels[i] = -1  # noise
            else:
                labels[i] = cluster_id
                queue = list(neighbors)
                while queue:
                    curr = queue.pop(0)
                    if labels[curr] == -1:
                        labels[curr] = cluster_id
                    elif labels[curr] == -1:
                        labels[curr] = cluster_id
                        curr_neighbors = [k for k in range(n) if self._distance_m(points[curr], points[k]) <= self.eps_meters]
                        if len(curr_neighbors) >= self.min_samples:
                            queue.extend(curr_neighbors)
                cluster_id += 1
        return labels
