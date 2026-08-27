from rest_framework import serializers
from .models import Complaint, ComplaintCategory, ComplaintAttachment, ComplaintAssignment, Resolution, ResolutionEvidence, Feedback, ChatMessage
from .validators import validate_file_size, validate_mime_type

class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory
        fields = '__all__'

class ComplaintAttachmentSerializer(serializers.ModelSerializer):
    # Using DRF FileField for validation during upload, but saving as URL later if using S3
    file = serializers.FileField(validators=[validate_file_size, validate_mime_type], write_only=True, required=False)
    
    class Meta:
        model = ComplaintAttachment
        fields = ['id', 'file_url', 'file_type', 'file']
        read_only_fields = ['file_url']

class ComplaintSerializer(serializers.ModelSerializer):
    attachments = ComplaintAttachmentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Complaint
        fields = ['id', 'title', 'description', 'priority', 'status', 'ai_confidence_score', 'category', 'category_name', 'attachments', 'created_at', 'updated_at']
        read_only_fields = ['status', 'ai_confidence_score', 'citizen']

class ComplaintAssignmentSerializer(serializers.ModelSerializer):
    staff_email = serializers.CharField(source='staff.user.email', read_only=True)
    
    class Meta:
        model = ComplaintAssignment
        fields = '__all__'

class ResolutionEvidenceSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[validate_file_size, validate_mime_type], write_only=True, required=False)
    
    class Meta:
        model = ResolutionEvidence
        fields = ['id', 'file_url', 'description', 'file']

class ResolutionSerializer(serializers.ModelSerializer):
    evidence = ResolutionEvidenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resolution
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'complaint', 'sender', 'sender_email', 'content', 'is_read', 'created_at']
        read_only_fields = ['complaint']
