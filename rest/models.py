from django.db import models

from rest.managers import RestManager


class RestModel(models.Model):

    PRIVY_FIELDS = []

    objects = RestManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._forced = {}

    class Meta:
        abstract = True
