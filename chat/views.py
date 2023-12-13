from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.paginations import DefaultPagination, PaginationHandlerMixin
from .models import ChatRoom, Message
from .serializers import MessageSerializer, ChatRoomSerializer,ChatRoomPostSerializer

from drf_yasg.utils import swagger_auto_schema


# register staff from tenant view


class CreateChatRoomView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_summary="Endpoint to create chat room")
    def post(self, request):
        data = request.data
        chat_slug = data["name"].replace(" ", "_").lower()
        serializer = ChatRoomPostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(slug=chat_slug)
            return Response(
                {
                    "status": True,
                    "msg": "chat room created",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)


class ChatRoomsView(APIView, PaginationHandlerMixin):
    permission_classes = (AllowAny,)
    pagination_class = DefaultPagination

    @swagger_auto_schema(operation_summary="Endpoint to list chat room")
    def get(self, request):
        chat_rooms = ChatRoom.objects.all()
        page = self.paginate_queryset(chat_rooms)
        if page is not None:
            serializer = ChatRoomSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ChatRoomSerializer(self.get_queryset(), many=True)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class ChatRoomView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(operation_summary="Endpoint to get single chat room")
    def get(self, request, name=None):
        chat_room_name = name.replace("_", " ")
        if name:
            chat_rooms = ChatRoom.objects.get(name=chat_room_name)
            serializer = ChatRoomSerializer(chat_rooms)
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )


class ChatRoomAgentView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Endpoint to get single chat room agent view"
    )
    def get(self, request, slug):
        if slug:
            chat_rooms = ChatRoom.objects.get(slug=slug)
            serializer = ChatRoomSerializer(chat_rooms)
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )


class MessageView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_summary="Endpoint to list messages")
    def get(self, request, slug=None):
        chat_room = ChatRoom.objects.get(slug=slug)
        messages = Message.objects.filter(chat_room=chat_room)[0:25]
        serializer = MessageSerializer(messages, many=True)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )
