from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonplaceUser(models.Model):
    """Commonplace User, connected to auth_user table"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
