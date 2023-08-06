"""Authentication module."""

from typing import Union

from flask_jwt_extended import JWTManager
from redis import Redis

from notelist.config import sm
from notelist.models.users import User
from notelist.responses import (
    ResponseData, MV_MISSING_TOKEN, MV_INVALID_TOKEN, MV_NOT_FRESH_TOKEN,
    MV_EXPIRED_TOKEN, MV_REVOKED_TOKEN, MT_ERROR_MISSING_TOKEN,
    MT_ERROR_INVALID_TOKEN, MT_ERROR_NOT_FRESH_TOKEN, MT_ERROR_EXPIRED_TOKEN,
    MT_ERROR_REVOKED_TOKEN, get_response_data)


JwtData = dict[str, Union[int, str]]

# JWT object
jwt = JWTManager()

# Block List Redis database client. By setting "decode_responses" to True,
# calls to "blocklist_redis.get" will return a string value instead of bytes.
blocklist_redis = Redis(
    sm.get("NOTELIST_REDIS_HOST"),
    sm.get("NOTELIST_REDIS_PORT"),
    sm.get("NOTELIST_REDIS_BLOCKLIST_DB"),
    sm.get("NOTELIST_REDIS_PASSWORD"),
    decode_responses=True)


@jwt.unauthorized_loader
def unauthorized_loader(error: str) -> ResponseData:
    """Handle requests with no JWT.

    :param error: Error message.
    :return: Response data dictionary.
    """
    return get_response_data(MV_MISSING_TOKEN, MT_ERROR_MISSING_TOKEN), 401


@jwt.invalid_token_loader
def invalid_token_loader(error: str) -> ResponseData:
    """Handle requests with an invalid JWT.

    :param error: Error message.
    :return: Response data dictionary.
    """
    return get_response_data(MV_INVALID_TOKEN, MT_ERROR_INVALID_TOKEN), 422


@jwt.needs_fresh_token_loader
def needs_fresh_token_loader(
    header: JwtData, payload: JwtData
) -> ResponseData:
    """Handle requests with a not fresh JWT.

    :param header: JWT header data.
    :param payload: JWT payload data.
    :return: Response data dictionary.
    """
    return get_response_data(MV_NOT_FRESH_TOKEN, MT_ERROR_NOT_FRESH_TOKEN), 401


@jwt.expired_token_loader
def expired_token_loader(header: JwtData, payload: JwtData) -> ResponseData:
    """Handle requests with an expired JWT.

    :param header: JWT header data.
    :param payload: JWT payload data.
    :return: Response data dictionary.
    """
    return get_response_data(MV_EXPIRED_TOKEN, MT_ERROR_EXPIRED_TOKEN), 401


@jwt.revoked_token_loader
def revoked_token_loader(header: JwtData, payload: JwtData) -> ResponseData:
    """Handle requests with a revoked JWT.

    :param header: JWT header data.
    :param payload: JWT payload data.
    :return: Response data dictionary.
    """
    return get_response_data(MV_REVOKED_TOKEN, MT_ERROR_REVOKED_TOKEN), 401


@jwt.token_in_blocklist_loader
def blocklist_loader(header: JwtData, payload: JwtData) -> bool:
    """Check if a JWT has been revoked.

    :param header: JWT header data.
    :param payload: JWT payload data.
    :return: Whether the given JWT has been revoked or not.
    """
    # JTI is a unique identifier of the JWT token
    return blocklist_redis.get(payload["jti"]) is not None


@jwt.additional_claims_loader
def additional_claims_loader(identity: str) -> dict[str, bool]:
    """Add additional information to the JWT payload when creating a JWT.

    :param identity: JWT identity. In this case, it's the user ID.
    :return: Dictionary with additional information about the request user.
    """
    user = User.get_by_id(identity)
    return {"user_id": user.id, "admin": user.admin}
