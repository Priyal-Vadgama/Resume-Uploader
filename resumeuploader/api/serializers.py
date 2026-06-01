from rest_framework import serializers
from api.models import Profile, CandidateList

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']

class CandidateListSerializer(serializers.ModelSerializer):
    candidates = Profileserializer(many=True, read_only=True)

    class Meta:
        model = CandidateList
        fields = ['id', 'title', 'description', 'candidates', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']