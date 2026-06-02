from rest_framework.response import Response
from api.models import Profile, CandidateList
from api.serializers import Profileserializer, CandidateListSerializer
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
class ProfileView(APIView):
    def post(self, request, format=None):
        serializer = Profileserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Resume uploaded successfully','status':'success', 'candidate':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.error)

    def get(self, request, pk=None, format=None):
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
