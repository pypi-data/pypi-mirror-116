"""User schemas module."""

from marshmallow import ValidationError
from flask_marshmallow.fields import fields

from notelist import tools
from notelist.db import ma
from notelist.models.users import MIN_PASSWORD, MAX_PASSWORD
from notelist.models.users import User


INVALID_VALUE = "Invalid value."


class UserSchema(ma.SQLAlchemyAutoSchema):
    """User schema."""

    class Meta:
        """User schema metadata."""

        model = User
        fields = [
            "id", "username", "password", "admin", "enabled", "name", "email",
            "created_ts", "last_modified_ts"]
        load_only = ["password"]
        dump_only = ["id", "created_ts", "last_modified_ts"]
        ordered = True
        load_instance = True

    password = fields.Method(None, "load_password", required=True)

    def load_password(self, val: str) -> str:
        """Deserialize the user's password."""
        ok = False

        if type(val) == str:
            val = val.strip()
            c = len(val)
            ok = c >= MIN_PASSWORD and c <= MAX_PASSWORD

        if not ok:
            raise ValidationError({"password": INVALID_VALUE})

        return tools.get_hash(val)
