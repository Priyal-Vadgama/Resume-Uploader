from rest_framework import serializers
from api.models import Profile, CandidateList

class Profileserializer(serializers.ModelSerializer):
    """DRF serializer for the Profile model.

    Serializes all candidate profile fields including optional image
    and resume file uploads for API request/response handling.
    """

    class Meta:
        model=Profile
        fields = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']

class CandidateListSerializer(serializers.ModelSerializer):
    """DRF serializer for the CandidateList model.

    Includes a nested ``Profileserializer`` for the many-to-many
    ``candidates`` relation so that full profile data is returned
    inline with each candidate list.
    """

    candidates = Profileserializer(many=True, read_only=True)

    class Meta:
        model = CandidateList
        fields = ['id', 'title', 'description', 'candidates', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
