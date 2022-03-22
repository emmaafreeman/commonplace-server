from django.db import models
from .commonplace_user import CommonplaceUser


class Entry(models.Model):
    """Model for Commonplace Entries"""

    user = models.ForeignKey(CommonplaceUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, null=True)
    body = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
