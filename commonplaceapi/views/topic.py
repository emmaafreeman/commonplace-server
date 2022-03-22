"""View module for handling requests about events"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from commonplaceapi.models import Topic, CommonplaceUser, Entry

User = get_user_model()


class TopicView(ViewSet):
    """ Commonplace Topic Viewset"""

    def create(self, request):
        """Handle POST operations for Topics

        Returns:
            Response -- JSON serialized Topic instance
        """

        # Get user object of currently authenticated user
        user = CommonplaceUser.objects.get(user=request.auth.user)

        # Create new Topic instance and set fields equal to data entered by user
        topic = Topic()
        topic.name = request.data["name"]
        
        # Assign current user data to new entry
        topic.user = user
        
        try:
            # Save new topic
            topic.save()

            # Determine which serializer to use and return 201 status
            serializer = TopicSerializer(topic, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Handle exceptions
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Topic

        Returns:
            Response -- JSON serialized Entry instance
        """
        try:
            # Get topic by id
            topic = Topic.objects.get(pk=pk)

            # Determine which serializer to use and return requested topic
            serializer = TopicSerializer(topic, context={'request': request})
            return Response(serializer.data)
        
        # Handle exceptions
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Topic

        Returns:
            Response -- Empty body with 204 status code
        """
        
        # Get user object of currently authenticated user
        user = CommonplaceUser.objects.get(user=request.auth.user)
        
        # Get topic by id
        topic = Topic.objects.get(pk=pk)
        
        # Set fields equal to new data entered by user
        topic.name = request.data["name"]
        
        # Assign current user data to topic
        topic.user = user

        # Save changes to topic
        topic.save()

        # Return 204
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a Topic

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:

            # Get entry by id
            topic = Topic.objects.get(pk=pk)

            # Delete specified entry
            topic.delete()

            # Return 204
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        # Return 404 if entry does not exist
        except Topic.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # Handle other exceptions
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Topics resource

        Returns:
            Response -- JSON serialized list of Topics
        """
        # Get all topics from the database
        topics = Topic.objects.all()

        # Determine which serializer to use and return requested topics
        serializer = TopicSerializer(
            topics, many=True, context={'request': request})
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
          'body', 'created_on')
