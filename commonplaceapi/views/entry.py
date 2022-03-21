"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from commonplaceapi.models import Entry, CommonplaceUser, Topic
from django.db.models import Q

class EntryView(ViewSet):
    """ Commonplace Entry Viewset"""

    def create(self, request):
        """Handle POST operations for Entries

        Returns:
            Response -- JSON serialized Entry instance
        """
        user = CommonplaceUser.objects.get(user=request.auth.user)

        entry = Entry()
        entry.title = request.data["title"]
        entry.body = request.data["body"]
        entry.user = user

        try:
            entry.save()
            entry.entry_topics.set(request.data["entry_topics"])
            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Entry

        Returns:
            Response -- JSON serialized Entry instance
        """
        try:
            entry = Entry.objects.get(pk=pk)
            serializer = EntrySerializer(entry, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for an Entry

        Returns:
            Response -- Empty body with 204 status code
        """
        user = CommonplaceUser.objects.get(user=request.auth.user)

        entry = Entry.objects.get(pk=pk)
        entry.title = request.data["title"]
        entry.body = request.data["body"]
        entry.user = user
        entry.entry_topics.set(request.data["entry_topics"])


        entry.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for an Entry

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            entry = Entry.objects.get(pk=pk)
            entry.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Entry.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Entries resource

        Returns:
            Response -- JSON serialized list of Entries
        """
        user = CommonplaceUser.objects.get(user=request.auth.user)

        current_user_id = user.id


        # Get all game records from the database
        entries = Entry.objects.all()
        
        if current_user_id is not None:
            entries = entries.filter(user_id=current_user_id)
        
        title_query = self.request.query_params.get('title', None)
        body_query = self.request.query_params.get('body', None)
        
        if title_query and body_query is not None:
            entries = entries.filter(Q(title__contains=title_query) | Q(body__contains=body_query))
        
        # if body_query is not None:
        #     entries = entries.filter(body__contains=body_query)
       
        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # game_type = self.request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(game_type__id=game_type)

        serializer = EntrySerializer(
            entries, many=True, context={'request': request})
        return Response(serializer.data)
    
    # def list(self, request):
    #     """Handle GET requests to events resource

    #     Returns:
    #         Response -- JSON serialized list of events
    #     """
    #     # Get the current authenticated user
    #     user = CommonplaceUser.objects.get(user=request.auth.user)
    #     entries = Entry.objects.all()
    #     title_query = self.request.query_params.get('title', None)
    #     body_query = self.request.query_params.get('body', None)
        
    #     if title_query is not None:
    #         entries = entries.filter(title=title_query)
        
    #     if body_query is not None:
    #         entries = entries.filter(body=body_query)

    #     serializer = EntrySerializer(
    #         entries, many=True, context={'request': request})
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
