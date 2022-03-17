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
        
        # entry_topics = Topic.objects.get(pk=request.data["gameTypeId"])
        # topic.entry_topics = game_type

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

        topic = Topic()
        topic.name = request.data["name"]

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
        entries = Topic.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(game_type__id=game_type)

        serializer = TopicSerializer(
            entries, many=True, context={'request': request})
        return Response(serializer.data)

        
    #MAY NEED THIS TO FILTER BY TOPIC
    # def list(self, request):
    #     """Handle GET requests to events resource

    #     Returns:
    #         Response -- JSON serialized list of events
    #     """
    #     # Get the current authenticated user
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     events = Event.objects.all()

    #     # Set the `joined` property on every event
    #     for event in events:
    #         if gamer in event.attendees.all():
    #         # Check to see if the gamer is in the attendees list on the event
    #             event.joined = True

    #     # Support filtering events by game
    #     game = self.request.query_params.get('gameId', None)
    #     if game is not None:
    #         events = events.filter(game__id=type)

    #     serializer = EventSerializer(
    #         events, many=True, context={'request': request})
    #     return Response(serializer.data)
 
    # @action(methods=['post', 'delete'], detail=True)
    # def signup(self, request, pk=None):
    #     """Managing gamers signing up for events"""
    #     # Django uses the `Authorization` header to determine
    #     # which user is making the request to sign up
    #     gamer = Gamer.objects.get(user=request.auth.user)

    #     try:
    #         # Handle the case if the client specifies a game
    #         # that doesn't exist
    #         event = Event.objects.get(pk=pk)
    #     except Event.DoesNotExist:
    #         return Response(
    #             {'message': 'Event does not exist.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # A gamer wants to sign up for an event
    #     if request.method == "POST":
    #         try:
    #             # Using the attendees field on the event makes it simple to add a gamer to the event
    #             # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
    #             event.attendees.add(gamer)
    #             return Response({}, status=status.HTTP_201_CREATED)
    #         except Exception as ex:
    #             return Response({'message': ex.args[0]})

    #     # User wants to leave a previously joined event
    #     elif request.method == "DELETE":
    #         try:
    #             # The many to many relationship has a .remove method that removes the gamer from the attendees list
    #             # The method deletes the row in the join table that has the gamer_id and event_id
    #             event.attendees.remove(gamer)
    #             return Response(None, status=status.HTTP_204_NO_CONTENT)
    #         except Exception as ex:
    #             return Response({'message': ex.args[0]})


class EventUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# class EventGamerSerializer(serializers.ModelSerializer):
#     """JSON serializer for event organizer"""
#     user = EventUserSerializer(many=False)

#     class Meta:
#         model = Gamer
#         fields = ['user']

class EntrySerializer(serializers.ModelSerializer):
    """JSON serializer for events"""

    # USE THIS FOR TOPICS LATER
    # organizer = EventGamerSerializer(many=False)
    # game = GameSerializer(many=False)
    user = EventUserSerializer(many=False)

    class Meta:
        model = Entry
        fields = ('id', 'user', 'title',
          'body', 'created_on')


class TopicSerializer(serializers.ModelSerializer):
    """JSON serializer for topics"""
    class Meta:
        model = Topic
        fields = ('id', 'name')