from rest_framework import serializers
from api.models import Profile, CandidateList, Skill

class Profileserializer(serializers.ModelSerializer):
    """DRF serializer for the Profile model.

    Serializes all candidate profile fields including optional image
    and resume file uploads for API request/response handling.
    """

    class Meta:
        model=Profile
        fields = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location', 'pimage', 'resume']

class SkillSerializer(serializers.ModelSerializer):
    """DRF serializer for the Skill model.

    Serializes skill name, proficiency level, and years of experience
    for API request/response handling. The ``profile`` field is
    write-only so that skills are always scoped to a specific candidate.
    """

    proficiency_display = serializers.CharField(
        source='get_proficiency_display',
        read_only=True,
    )

    class Meta:
        model = Skill
        fields = [
            'id', 'profile', 'name', 'proficiency',
            'proficiency_display', 'years_experience',
        ]
        read_only_fields = ['id']


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
