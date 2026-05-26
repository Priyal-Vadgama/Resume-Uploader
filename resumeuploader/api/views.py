from rest_framework.response import Response
from api.models import Profile
from api.serializers import Profileserializer
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