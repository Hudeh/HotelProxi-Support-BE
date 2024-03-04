from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    ContactUsSerializers,
    NewsLetterSerializers,
)
from .tasks import send_contact_form_task, send_respond_contact_form_task
from drf_yasg.utils import swagger_auto_schema


#  contact us form
class ContactUSAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        contact_email = request.data.get("email")
        contact_name = request.data.get("name")
        data = {
            "email": contact_email,
            "name": contact_name,
        }
        serializer = ContactUsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_respond_contact_form_task.delay(data)
            send_contact_form_task.delay(request.data)
            return Response(
                {
                    "status": True,
                    "msg": "Thanks for being awesome! We have received your message.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": False,
                "msg": "Error pls check you sending the right information.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# NEWSLETTER
class NewsLetterAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = NewsLetterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "msg": "Thanks for being awesome! We have received your message.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": False,
                "msg": "Error pls check you sending the right information.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )