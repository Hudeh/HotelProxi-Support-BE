from rest_framework import serializers
from .models import ContactUs, NewsLetter


class ContactUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ("name", "email", "phone", "subject", "message")


class NewsLetterSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = ("email",)
