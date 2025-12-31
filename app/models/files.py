from tortoise import fields
from tortoise.models import Model
from app.constants import FileTypeEnum, FileExtensionEnum, AccessType

class FileModel(Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=255)
    original_filename = fields.CharField(max_length=255)
    mime_type = fields.CharField(max_length=127, null=True)
    type = fields.CharEnumField(enum_type=FileTypeEnum)
    extension = fields.CharEnumField(
        enum_type=FileExtensionEnum,
        null=True
    )
    file_path = fields.CharField(max_length=250)
    owner = fields.ForeignKeyField(
        "models.UserModel",
        related_name="owner",
        on_delete=fields.CASCADE,
    )
    size = fields.FloatField()

    metadata = fields.JSONField(default=dict)  # Store additional file metadata

    access_type = fields.CharEnumField(
        enum_type=AccessType
    )
    shared_with = fields.JSONField(default=list)  # List of user IDs

    is_deleted = fields.BooleanField(default=False)
    deleted_at = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    

