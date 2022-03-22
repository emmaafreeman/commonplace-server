from django.db import models
from .entry import Entry
from .commonplace_user import CommonplaceUser


class Topic(models.Model):
    """Model for Entry Topics"""

    user = models.ForeignKey(CommonplaceUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    assign_to_entry = models.ManyToManyField(Entry, related_name='entry_topics')
