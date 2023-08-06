from django.contrib.auth.models import User
import json
from django.db import models
from pyzstd import decompress, compress
from base64 import b64encode, b64decode


class TextChoices(models.TextChoices):
    @classmethod
    def list_codes(cls):
        return [code for code, label in cls.choices]


class AbstractCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField("crée le", auto_now_add=True)
    updated_at = models.DateTimeField("maj le", auto_now=True)

    class Meta:
        abstract = True


class AbstractSsoUser(AbstractCreatedUpdatedModel, models.Model):
    sso_uuid = models.CharField(max_length=100, db_index=True)
    list_apps = models.JSONField()
    user = models.OneToOneField(User, related_name="sso_user", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Reference(AbstractCreatedUpdatedModel):
    code = models.CharField(max_length=20, primary_key=True)
    label = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ["label"]

    def __str__(self):
        return self.label


class CompressedJsonField(models.JSONField):
    description = "Compress Json field - specially used for logs fields"

    def from_db_value(self, value, expression, connection):
        compressed_value = json.loads(value)["data"]
        return super().from_db_value(
            decompress(b64decode(compressed_value)), expression, connection
        )

    def get_prep_value(self, value):
        value_to_compress = super().get_prep_value(value)
        compressed_value = compress(value_to_compress.encode("utf-8"))
        return json.dumps({"data": b64encode(compressed_value).decode("utf-8")})
