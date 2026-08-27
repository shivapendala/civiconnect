import math
from typing import List, Tuple, Dict

class DistanceMatrixCalculator:
    """Calculates all-pairs pairwise geodesic distance matrices for fleet dispatch and TSP heuristics."""
    
    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        )
        return 2 * r * math.asin(math.sqrt(a))

    @classmethod
    def compute_matrix(cls, locations: List[Tuple[float, float]]) -> List[List[float]]:
        n = len(locations)
        matrix = [[0.0] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = cls.haversine(locations[i][0], locations[i][1], locations[j][0], locations[j][1])
                matrix[i][j] = round(dist, 3)
                matrix[j][i] = round(dist, 3)
                
        return matrix
