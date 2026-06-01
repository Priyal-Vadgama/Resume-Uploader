"""NoSQL-backed API views for the Resume Uploader.

Provides MongoDB-backed alternatives to the SQL-based views in ``api.views``.
When MongoDB is configured, these views handle profile storage and retrieval
through PyMongo instead of the Django ORM, enabling flexible schema designs,
horizontal scaling, and embedded sub-documents for resume data.

Usage::

    from api.nosql_views import ProfileNoSQLView

    urlpatterns = [
        path('resume/nosql/', ProfileNoSQLView.as_view()),
    ]
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProfileNoSQLView(APIView):
    """MongoDB-backed API endpoint for candidate profile management.

    Provides a NoSQL alternative to :class:`api.views.ProfileView` that
    stores candidate profiles as MongoDB documents rather than SQL rows.
    Supports POST (create), GET (list or retrieve by document id), and
    DELETE operations on profiles stored in a MongoDB collection.

    Attributes:
        collection_name: MongoDB collection used for profile storage.
        db_name: MongoDB database name, configurable via settings.
    """

    collection_name = 'candidate_profiles'
    db_name = 'resumeuploader'

    def _get_collection(self):
        """Return the MongoDB collection handle for profile documents.

        Lazily initialises a PyMongo client and returns the configured
        collection. In production the connection parameters should be
        sourced from ``django.conf.settings``.

        Returns:
            pymongo.collection.Collection: The candidate profiles collection.

        Raises:
            ImportError: If PyMongo is not installed.
        """
        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "PyMongo is required for NoSQL views. "
                "Install it with: pip install pymongo"
            )
        client = MongoClient('localhost', 27017)
        db = client[self.db_name]
        return db[self.collection_name]

    def post(self, request, format=None):
        """Create a new candidate profile as a MongoDB document.

        Accepts JSON with candidate fields (name, email, dob, state,
        gender, location) and optional pimage and resume paths.
        Returns the created document with its generated ``_id``.

        Args:
            request: DRF Request object with JSON body.
            format: Optional content-type suffix.

        Returns:
            Response: JSON containing status and the created document.
        """
        collection = self._get_collection()
        document = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'dob': request.data.get('dob'),
            'state': request.data.get('state'),
            'gender': request.data.get('gender'),
            'location': request.data.get('location'),
            'pimage': request.data.get('pimage', ''),
            'resume': request.data.get('resume', ''),
        }
        # Convert _id to string so it is JSON-serializable
        result = collection.insert_one(document)
        document['_id'] = str(result.inserted_id)
        return Response(
            {
                'msg': 'Resume uploaded successfully',
                'status': 'success',
                'candidate': document,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, pk=None, format=None):
        """Retrieve a single profile by document id or list all profiles.

        When ``pk`` is provided, looks up the profile by its MongoDB
        ObjectId string. Otherwise returns all documents in the
        collection.

        Args:
            request: DRF Request object.
            pk: Optional MongoDB ObjectId as a 24-character hex string.
            format: Optional content-type suffix.

        Returns:
            Response: JSON containing the requested profile(s).
        """
        collection = self._get_collection()
        if pk:
            from bson import ObjectId
            try:
                document = collection.find_one({'_id': ObjectId(pk)})
            except Exception:
                return Response(
                    {'error': 'Invalid profile id format'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if document is None:
                return Response(
                    {'error': 'Candidate not found'},
                    status=status.HTTP_404_NOT_FOUND,
                )
            document['_id'] = str(document['_id'])
            return Response(
                {'status': 'success', 'candidate': document},
                status=status.HTTP_200_OK,
            )

        documents = list(collection.find())
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return Response(
            {'status': 'success', 'candidates': documents},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk=None):
        """Delete a candidate profile by MongoDB document id.

        Removes the matching document from the collection. The
        associated file uploads on disk are not cleaned up by this
        endpoint.

        Args:
            request: DRF Request object.
            pk: MongoDB ObjectId as a 24-character hex string.

        Returns:
            Response: JSON confirmation message.
        """
        from bson import ObjectId
        collection = self._get_collection()
        try:
            result = collection.delete_one({'_id': ObjectId(pk)})
        except Exception:
            return Response(
                {'error': 'Invalid profile id format'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if result.deleted_count == 0:
            return Response(
                {'error': 'Candidate not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response({'msg': 'Data Deleted Successfully'})
