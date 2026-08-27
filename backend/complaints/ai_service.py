import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import F

from complaints.models import Complaint, ComplaintCategory, ComplaintPriority
from complaints.services import calculate_distance

class CivicAIModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.category_classifier = MultinomialNB()
        self.is_trained = False
        self._mock_training_data()
        
    def _mock_training_data(self):
        """
        Train the model on some initial mock data. In a real scenario, this would load 
        a pre-trained model from disk or train on the historical database.
        """
        training_texts = [
            "street light is not working near my house",
            "pothole on main street causing accidents",
            "water leaking from the main pipe in the avenue",
            "garbage has not been collected for a week",
            "power outage in the entire block",
            "huge pothole damaging cars",
            "no water supply since morning",
            "trash bins are overflowing",
            "broken streetlight on the highway",
            "live electrical wire fallen on road"
        ]
        
        # We assume these categories exist in DB, if not we fall back to generic mappings
        training_labels = [
            "Electricity", "Road", "Water", "Sanitation", "Electricity",
            "Road", "Water", "Sanitation", "Electricity", "Electricity"
        ]
        
        X = self.vectorizer.fit_transform(training_texts)
        self.category_classifier.fit(X, training_labels)
        self.is_trained = True

    def predict_category(self, description):
        """
        Predicts the category of a complaint based on its description.
        Returns the predicted category name and the confidence score (0 to 1).
        """
        if not self.is_trained:
            return None, 0.0
            
        X = self.vectorizer.transform([description])
        prediction = self.category_classifier.predict(X)[0]
        
        # Get probability of the predicted class
        probs = self.category_classifier.predict_proba(X)[0]
        confidence = max(probs)
        
        return prediction, confidence

    def predict_priority(self, description, category_name, latitude=None, longitude=None):
        """
        Predicts the priority (LOW, MEDIUM, HIGH, CRITICAL).
        Simple rule-based combined with keywords for demonstration.
        """
        desc_lower = description.lower()
        
        critical_keywords = ['live wire', 'accident', 'fire', 'emergency', 'death', 'blood']
        high_keywords = ['not working', 'no water', 'outage', 'huge', 'broken']
        
        if any(kw in desc_lower for kw in critical_keywords):
            return ComplaintPriority.CRITICAL
            
        if any(kw in desc_lower for kw in high_keywords):
            return ComplaintPriority.HIGH
            
        if category_name in ['Electricity', 'Water']:
            # Utility issues default to high if not specified
            return ComplaintPriority.HIGH
            
        return ComplaintPriority.MEDIUM

    def detect_duplicate(self, new_description, new_lat=None, new_lon=None, similarity_threshold=0.85, distance_threshold_km=0.5):
        """
        Compares new complaint against existing complaints.
        Returns: is_duplicate (bool), max_similarity (float), duplicate_complaint_id (int or None)
        """
        # Get recent complaints (e.g., last 30 days, or just all for this demo)
        recent_complaints = Complaint.objects.all().order_by('-created_at')[:100]
        
        if not recent_complaints.exists():
            return False, 0.0, None
            
        # Extract texts
        complaint_texts = [c.description for c in recent_complaints]
        complaint_ids = [c.id for c in recent_complaints]
        
        # Include the new description as the first element for vectorization
        all_texts = [new_description] + complaint_texts
        tfidf_matrix = self.vectorizer.transform(all_texts)
        
        # Compute cosine similarity between new description (index 0) and all others
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Find the max similarity
        max_idx = np.argmax(similarities)
        max_sim = similarities[max_idx]
        
        if max_sim >= similarity_threshold:
            potential_duplicate_id = complaint_ids[max_idx]
            
            # Further filter by location if coordinates are provided
            if new_lat and new_lon:
                dup = Complaint.objects.get(id=potential_duplicate_id)
                if hasattr(dup, 'location'):
                    dist = calculate_distance(new_lat, new_lon, float(dup.location.latitude), float(dup.location.longitude))
                    if dist <= distance_threshold_km:
                        return True, max_sim, potential_duplicate_id
                    else:
                        # Texts are similar, but locations are far apart
                        return False, max_sim, None
            else:
                # No location data, rely purely on text
                return True, max_sim, potential_duplicate_id
                
        return False, max_sim, None

# Singleton instance for the service
ai_engine = CivicAIModel()
