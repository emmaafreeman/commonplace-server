"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from commonplaceapi.models import Topic, CommonplaceUser, Entry

class TopicView(ViewSet):
    """ Commonplace Topic Viewset"""

    def create(self, request):
        """Handle POST operations for Topics

        Returns:
            Response -- JSON serialized Topic instance
        """

        user = CommonplaceUser.objects.get(user=request.auth.user)

        topic = Topic()
        topic.name = request.data["name"]
        topic.user = user
        
        try:
            topic.save()
            serializer = TopicSerializer(topic, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Topic

        Returns:
            Response -- JSON serialized Entry instance
        """
        try:
            topic = Topic.objects.get(pk=pk)
            serializer = TopicSerializer(topic, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Topic

        Returns:
            Response -- Empty body with 204 status code
        """
        user = CommonplaceUser.objects.get(user=request.auth.user)
        
        topic = Topic.objects.get(pk=pk)
        topic.name = request.data["name"]
        topic.user = user

        topic.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a Topic

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            topic = Topic.objects.get(pk=pk)
            topic.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Topic.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Topics resource

        Returns:
            Response -- JSON serialized list of Topics
        """
        # Get all game records from the database
        topics = Topic.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(game_type__id=game_type)

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
