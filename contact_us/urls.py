from django.urls import re_path as _
from .views import *


urlpatterns = [
    _(r"^contact_us", ContactUSAPI.as_view(), name="contact_us"),
    _(r"^newsletter", NewsLetterAPI.as_view(), name="newsletter")
]
