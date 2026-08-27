import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Complaint
from django.db.models import Q

def analyze_complaint_image(complaint_id):
    """
    Mock Computer Vision function that would normally use an API like Google Cloud Vision or OpenAI Vision.
    It analyzes the attached images to identify the core issue, extract text, and estimate severity.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        
        # MOCK VISION RESPONSE
        vision_insights = {
            "detected_objects": ["Pothole", "Asphalt", "Water"],
            "severity_estimate": "High",
            "damage_area_sq_meters": 1.2,
            "extracted_text": "",
            "confidence": 0.89
        }
        
        # Update insights
        current_insights = complaint.ai_insights or {}
        current_insights['vision_analysis'] = vision_insights
        
        complaint.ai_insights = current_insights
        complaint.ai_confidence_score = vision_insights['confidence']
        complaint.save()
        return True
    except Complaint.DoesNotExist:
        return False


def find_similar_complaints_rag(complaint_id):
    """
    RAG (Retrieval-Augmented Generation) Chatbot Engine Mock.
    Uses TF-IDF and Cosine Similarity to find past resolved complaints that are semantically similar.
    In a real production app, this would use LangChain + OpenAI Embeddings + Pinecone/pgvector.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        
        # Only compare within same municipality and past resolved cases
        past_complaints = Complaint.objects.filter(
            municipality=complaint.municipality,
            status='RESOLVED'
        ).exclude(id=complaint_id)
        
        if not past_complaints.exists():
            return False
            
        corpus = [c.title + " " + c.description for c in past_complaints]
        ids = [c.id for c in past_complaints]
        
        # Add the target complaint
        target_text = complaint.title + " " + complaint.description
        corpus.append(target_text)
        
        # Vectorize
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate cosine similarity between target and all others
        similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
        
        # Get top 3 similar complaints
        top_indices = similarities.argsort()[-3:][::-1]
        
        similar_results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Threshold
                similar_results.append({
                    "complaint_id": str(ids[idx]),
                    "similarity_score": round(similarities[idx], 2),
                    "title": past_complaints[int(idx)].title
                })
        
        current_insights = complaint.ai_insights or {}
        
        # RAG Synthesis (Mock LLM Output)
        if similar_results:
            rag_summary = f"Found {len(similar_results)} similar past complaints. The usual resolution time for these is approx 4 days. Standard procedure: Dispatch maintenance crew for inspection."
        else:
            rag_summary = "No highly similar past complaints found."
            
        current_insights['rag_analysis'] = {
            "similar_cases": similar_results,
            "suggested_resolution_plan": rag_summary
        }
        
        complaint.ai_insights = current_insights
        complaint.save()
        return True
    except Complaint.DoesNotExist:
        return False
