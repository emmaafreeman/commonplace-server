from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from commonplaceapi.models import Entry, CommonplaceUser, Topic
from django.db.models import Q

User = get_user_model()


class EntryView(ViewSet):
    """ Commonplace Entry Viewset"""

    def create(self, request):
        """Handle POST operations for Entries

        Returns:
            Response -- JSON serialized Entry instance
        """
        # Get user object of currently authenticated user
        user = CommonplaceUser.objects.get(user=request.auth.user)

        # Create new Entry instance and set fields equal to data entered by user
        entry = Entry()
        entry.title = request.data["title"]
        entry.body = request.data["body"]
        
        # Assign current user data to new entry
        entry.user = user

        try:
            # Save new entry
            entry.save()

            # Set entry_topics field equal to data entered by user
            entry.entry_topics.set(request.data["entry_topics"])
            
            # Determine which serializer to use and return 201 status
            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Handle exceptions
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Entry

        Returns:
            Response -- JSON serialized Entry instance
        """
        try:
            # Get entry by id
            entry = Entry.objects.get(pk=pk)

            # Determine which serializer to use and return requested entry
            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data)
        
        # Return 404 if entry does not exist
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for an Entry

        Returns:
            Response -- Empty body with 204 status code
        """
        
        # Get user object of currently authenticated user
        user = CommonplaceUser.objects.get(user=request.auth.user)

        # Get entry by id
        entry = Entry.objects.get(pk=pk)
        
        # Set fields equal to new data entered by user
        entry.title = request.data["title"]
        entry.body = request.data["body"]
        entry.entry_topics.set(request.data["entry_topics"])

        # Assign current user data to entry
        entry.user = user

        # Save changes to entry
        entry.save()

        # Return 204
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an Entry

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            # Get entry by id
            entry = Entry.objects.get(pk=pk)

            # Delete specified entry
            entry.delete()

            # Return 204
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Return 404 if entry does not exist
        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # Handle other exceptions
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Entries resource

        Returns:
            Response -- JSON serialized list of Entries
        """
        
        # Get user object of currently authenticated user
        user = CommonplaceUser.objects.get(user=request.auth.user)

        # Get id of current user
        current_user_id = user.id

        # Get all game records from the database
        entries = Entry.objects.all()
        
        # Filter entries by user's id
        if current_user_id is not None:
            entries = entries.filter(user_id=current_user_id)
        
        # Get query params from request url
        title_query = self.request.query_params.get('title', None)
        body_query = self.request.query_params.get('body', None)
        
        # If query params are not None, filter entries if either title or body contain the params
        if title_query and body_query is not None:
            entries = entries.filter(Q(title__contains=title_query) | Q(body__contains=body_query))
        
        # Determine which serializer to use and return requested entries
        serializer = EntrySerializer(
            entries, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topics"""
    class Meta:
        model = Topic
        fields = ('id', 'name')


class EntrySerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    user = UserSerializer(many=False)
    entry_topics = TopicSerializer(many=True)

    class Meta:
        model = Entry
        fields = ('id', 'user', 'title',
          'body', 'created_on', 'entry_topics')
