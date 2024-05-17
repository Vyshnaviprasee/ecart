from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    STATUS_CHOICES = (
        (LIVE, "Live"),
        (DELETE, "Delete"),
    )
    name = models.CharField(max_length=120)
    address = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, related_name="customer", on_delete=models.CASCADE)
    phone = models.CharField(max_length=120)
    image = models.ImageField(blank=True, null=True, upload_to="customers/")
    email = models.EmailField()
    priority = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.user.username