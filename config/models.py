from django.db import models
from nanoid import generate


def generate_nanoid():
    return generate(size=12)


class TimestampModel(models.Model):
    id = models.CharField(
        max_length=12,
        primary_key=True,
        default=generate_nanoid,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
