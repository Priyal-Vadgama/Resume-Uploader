from rest_framework.response import Response
from api.models import Profile, CandidateList
from api.serializers import Profileserializer, CandidateListSerializer
from rest_framework.views import APIView
from rest_framework import status

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
        """
        if pk:
            try:
                candidate = Profile.objects.get(id=pk)
                serializer = Profileserializer(candidate)
                return Response({'status': 'success', 'candidate': serializer.data}, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            candidates = Profile.objects.all()
            serializer = Profileserializer(candidates, many=True)
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
        else:
            lists = CandidateList.objects.prefetch_related('candidates').all()
            serializer = CandidateListSerializer(lists, many=True)
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
