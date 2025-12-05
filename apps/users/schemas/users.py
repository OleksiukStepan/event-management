from drf_spectacular.utils import extend_schema

TAGS_USERS = ["Users"]

get_current_user = extend_schema(
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user.",
    tags=TAGS_USERS,
)

USER_SCHEMAS = {
    "current_user": get_current_user,
}
