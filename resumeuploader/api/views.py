from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Profile, CandidateList, Skill
from api.serializers import Profileserializer, CandidateListSerializer, SkillSerializer

# Create your views here.
class ProfileView(APIView):
    """API endpoint for managing individual candidate profiles.

    Supports POST (create), GET (list or retrieve by pk), and DELETE
    operations on the Profile model. Handles multipart form data for
    profile image and resume file uploads.
    """

    def post(self, request, format=None):
        """Create a new candidate profile with resume and image uploads.

        Accepts multipart/form-data with candidate fields, profile image,
        and resume file. Returns the created candidate data on success.
        """
        serializer = Profileserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Resume uploaded successfully','status':'success', 'candidate':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.error)

    def get(self, request, pk=None, format=None):
        """Retrieve a single profile by id or list all candidate profiles.

        When ``pk`` is provided, returns the matching Profile or a 404.
        Otherwise returns all Profile records.


        Supports optional query parameter filtering:
        - ``?name=<str>`` : exact match on name
        - ``?name__icontains=<str>`` : case-insensitive substring match on name
        - ``?email=<str>`` : exact match on email
        - ``?email__icontains=<str>`` : case-insensitive substring match on email
        - ``?state=<str>`` : exact match on state
        - ``?gender=<str>`` : exact match on gender
        - ``?location__icontains=<str>`` : case-insensitive substring match on location
        - ``?search=<str>`` : case-insensitive search across name, email, state, and location
        - ``?ordering=<field>`` : order by a field (prefix with ``-`` for descending, e.g. ``-dob``)
        """
        if pk:
            try:
                candidate = Profile.objects.get(id=pk)
                serializer = Profileserializer(candidate)
                return Response({'status': 'success', 'candidate': serializer.data}, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = Profile.objects.all()

        # --- Filtering ---
        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(name=name)

        name_icontains = request.query_params.get('name__icontains')
        if name_icontains:
            queryset = queryset.filter(name__icontains=name_icontains)

        email = request.query_params.get('email')
        if email:
            queryset = queryset.filter(email=email)

        email_icontains = request.query_params.get('email__icontains')
        if email_icontains:
            queryset = queryset.filter(email__icontains=email_icontains)

        state = request.query_params.get('state')
        if state:
            queryset = queryset.filter(state=state)

        gender = request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)

        location_icontains = request.query_params.get('location__icontains')
        if location_icontains:
            queryset = queryset.filter(location__icontains=location_icontains)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(email__icontains=search)
                | Q(state__icontains=search)
                | Q(location__icontains=search)
            )

        # --- Ordering ---
        ordering = request.query_params.get('ordering')
        valid_order_fields = ['id', 'name', 'email', 'dob', 'state', 'gender', 'location']
        if ordering:
            field = ordering.lstrip('-')
            if field in valid_order_fields:
                queryset = queryset.order_by(ordering)

        serializer = Profileserializer(queryset, many=True)
        return Response({'status': 'success', 'candidates': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """Delete a candidate profile by primary key.

        Removes the Profile record and its associated file uploads.
        Returns a success message on completion.
        """
        print(pk)
        id=pk
        candidate = Profile.objects.get(pk=id)
        candidate.delete()
        return Response({'msg':'Data Deleted Successfully'})

class CandidateListView(APIView):
    """API endpoint for managing curated candidate lists.

    Provides CRUD operations on CandidateList records, including
    associating existing Profile instances via a many-to-many
    relationship.
    """

    def post(self, request, format=None):
        """Create a new candidate list with optional associated profiles.

        Accepts JSON with title, description, and candidate IDs.
        Returns the created CandidateList on success.
        """
        serializer = CandidateListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'msg': 'Candidate list created successfully',
                 'status': 'success',
                 'candidate_list': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        """Retrieve a single candidate list by id or list all candidate lists.

        When ``pk`` is provided, returns the matching CandidateList with
        prefetched candidate profiles, or a 404. Otherwise returns all
        CandidateList records.


        Supports optional query parameter filtering:
        - ``?title=<str>`` : exact match on title
        - ``?title__icontains=<str>`` : case-insensitive substring match on title
        - ``?description__icontains=<str>`` : case-insensitive substring match on description
        - ``?search=<str>`` : case-insensitive search across both title and description
        - ``?ordering=<field>`` : order by a field (prefix with ``-`` for descending, e.g. ``-created_at``)
        """
        if pk:
            try:
                candidate_list = CandidateList.objects.prefetch_related('candidates').get(id=pk)
                serializer = CandidateListSerializer(candidate_list)
                return Response(
                    {'status': 'success', 'candidate_list': serializer.data},
                    status=status.HTTP_200_OK,
                )
            except CandidateList.DoesNotExist:
                return Response(
                    {'error': 'Candidate list not found'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        queryset = CandidateList.objects.prefetch_related('candidates').all()

        # --- Filtering ---
        title = request.query_params.get('title')
        if title:
            queryset = queryset.filter(title=title)

        title_icontains = request.query_params.get('title__icontains')
        if title_icontains:
            queryset = queryset.filter(title__icontains=title_icontains)

        description_icontains = request.query_params.get('description__icontains')
        if description_icontains:
            queryset = queryset.filter(description__icontains=description_icontains)

        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # --- Ordering ---
        ordering = request.query_params.get('ordering')
        valid_order_fields = ['title', 'created_at', 'updated_at']
        if ordering:
            field = ordering.lstrip('-')
            if field in valid_order_fields:
                queryset = queryset.order_by(ordering)

        serializer = CandidateListSerializer(queryset, many=True)
        return Response(
            {'status': 'success', 'candidate_lists': serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk=None, format=None):
        """Partially update an existing candidate list by primary key.

        Accepts a JSON partial update. Returns the updated CandidateList
        on success or a 404 if the list does not exist.
        """
        try:
            candidate_list = CandidateList.objects.get(id=pk)
        except CandidateList.DoesNotExist:
            return Response(
                {'error': 'Candidate list not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = CandidateListSerializer(candidate_list, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'msg': 'Candidate list updated successfully',
                 'status': 'success',
                 'candidate_list': serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Delete a candidate list by primary key.

        Removes the CandidateList record (the associated Profile
        instances are not deleted). Returns a 404 if not found.
        """
        try:
            candidate_list = CandidateList.objects.get(id=pk)
        except CandidateList.DoesNotExist:
            return Response(
                {'error': 'Candidate list not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        candidate_list.delete()
        return Response(
            {'msg': 'Candidate list deleted successfully', 'status': 'success'},
            status=status.HTTP_200_OK,
        )


class SkillView(APIView):
    """API endpoint for managing candidate skills and qualifications.

    Provides CRUD operations on the Skill model. Each skill is scoped
    to a candidate Profile via a foreign key. Supports listing,
    creating, retrieving by id, updating, and deleting skills.
    """

    def post(self, request, format=None):
        """Create a new skill record for a candidate.

        Accepts JSON with ``profile`` (id), ``name``, ``proficiency``,
        and ``years_experience``. Returns the created Skill on success.
        """
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'msg': 'Skill created successfully',
                    'status': 'success',
                    'skill': serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        """Retrieve a single skill by id or list all skills.

        When ``pk`` is provided, returns the matching Skill or a 404.
        Supports optional ``?profile=<id>`` query parameter to filter
        skills by candidate profile.
        """
        if pk:
            try:
                skill = Skill.objects.get(id=pk)
                serializer = SkillSerializer(skill)
                return Response(
                    {'status': 'success', 'skill': serializer.data},
                    status=status.HTTP_200_OK,
                )
            except Skill.DoesNotExist:
                return Response(
                    {'error': 'Skill not found'},
                    status=status.HTTP_404_NOT_FOUND,
                )

        queryset = Skill.objects.all()
        profile_id = request.query_params.get('profile')
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)

        serializer = SkillSerializer(queryset, many=True)
        return Response(
            {'status': 'success', 'skills': serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk=None, format=None):
        """Partially update an existing skill by primary key.

        Accepts a JSON partial update. Returns the updated Skill
        on success or a 404 if the skill does not exist.
        """
        try:
            skill = Skill.objects.get(id=pk)
        except Skill.DoesNotExist:
            return Response(
                {'error': 'Skill not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SkillSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'msg': 'Skill updated successfully',
                    'status': 'success',
                    'skill': serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """Delete a skill by primary key.

        Removes the Skill record. Returns a 404 if not found.
        """
        try:
            skill = Skill.objects.get(id=pk)
        except Skill.DoesNotExist:
            return Response(
                {'error': 'Skill not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        skill.delete()
        return Response(
            {'msg': 'Skill deleted successfully', 'status': 'success'},
            status=status.HTTP_200_OK,
        )
