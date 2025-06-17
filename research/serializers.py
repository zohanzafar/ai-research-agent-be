from rest_framework import serializers
from .models import ResearchResult

class ResearchRequestSerializer(serializers.Serializer):
    keyword = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True
    )

class ResearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchResult
        fields = [
            "id", "keyword", "scope", "design", "literature", "analysis",
            "discussion", "ethics", "references", "created_at"
        ]
