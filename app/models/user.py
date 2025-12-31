from tortoise import fields
from tortoise.models import Model
from app.constants import UserRoleType

class UserModel(Model):
    id = fields.IntField(primary_key=True, )
    fullname = fields.CharField(max_length=50)
    email = fields.CharField(unique=True, max_length=50)
    password = fields.CharField(max_length=100)
    role = fields.CharEnumField(
        enum_type=UserRoleType,
        default=UserRoleType.STANDARD.value,
        max_length=20
    )
    is_active = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(
        auto_now_add=True
    )
    updated_at = fields.DatetimeField(
        auto_now=True
    )

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.email} - {self.fullname}"
