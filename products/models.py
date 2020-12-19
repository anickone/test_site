from django.db import models
import uuid


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    logo = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    rotate_duration = models.FloatField(null=True, blank=True, editable=False)
    owner = models.ForeignKey(
        'auth.User',
        related_name='products',
        on_delete=models.CASCADE)
    modified = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)
