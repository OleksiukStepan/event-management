from drf_spectacular.utils import extend_schema

TAGS_AUTH = ["Authentication"]

register_user = extend_schema(
    summary="Register a new user",
    description="Create a new user account with username, email and password.",
    tags=TAGS_AUTH,
)

AUTH_SCHEMAS = {
    "register": register_user,
}
