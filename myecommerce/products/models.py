from django.db import models

class Product(models.Model):
    LIVE = 1
    DELETE = 0
    STATUS_CHOICES = (
        (LIVE, "Live"),
        (DELETE, "Delete"),
    )
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    image = models.ImageField(blank=True, null=True, upload_to="products/")
    priority = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title
