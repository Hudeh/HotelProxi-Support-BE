import uuid
from django.db import models
from utils.make_aware_timezone import timezone_aware
from report.models import generate_sku

class ContactUs(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    sku = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=18)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.sku is None:
            self.timestamp = timezone_aware()
            self.sku = generate_sku()
        super(ContactUs, self).save(*args, **kwargs)


class NewsLetter(models.Model):
    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    sku = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField()
    timestamp = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.sku is None:
            self.timestamp = timezone_aware()
            self.sku = generate_sku()
        super(NewsLetter, self).save(*args, **kwargs)
