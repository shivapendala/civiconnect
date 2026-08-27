import math
import hashlib
from typing import List, Dict, Tuple, Optional

class DeduplicationEngine:
    """Multi-modal complaint deduplication engine combining spatial proximity and image pHash."""
    
    @staticmethod
    def compute_phash(image_bytes: bytes) -> str:
        """Simulates 64-bit perceptual hash for fast Hamming distance lookup."""
        return hashlib.md5(image_bytes).hexdigest()[:16]

    @staticmethod
    def hamming_distance(hash1: str, hash2: str) -> int:
        return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

    @classmethod
    def evaluate_candidate(cls, lat1: float, lng1: float, hash1: Optional[str],
                           lat2: float, lng2: float, hash2: Optional[str],
                           max_distance_meters: float = 100.0) -> Tuple[bool, float]:
        # Spatial distance in meters
        dlat = (lat2 - lat1) * 111000.0
        dlng = (lng2 - lng1) * 111000.0 * math.cos(math.radians(lat1))
        dist_m = math.sqrt(dlat ** 2 + dlng ** 2)
        
        if dist_m > max_distance_meters:
            return False, 0.0
            
        spatial_sim = max(0.0, 1.0 - (dist_m / max_distance_meters))
        
        visual_sim = 0.5
        if hash1 and hash2 and len(hash1) == len(hash2):
            h_dist = cls.hamming_distance(hash1, hash2)
            visual_sim = max(0.0, 1.0 - (h_dist / len(hash1)))
            
        combined_score = 0.6 * spatial_sim + 0.4 * visual_sim
        is_dup = combined_score >= 0.75
        return is_dup, round(combined_score, 3)
