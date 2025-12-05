from drf_spectacular.utils import extend_schema

from apps.events.serializers import ParticipantSerializer

TAGS_REGISTRATION = ["Event Registration"]

list_participants = extend_schema(
    summary="List event participants",
    description="Get a list of all users registered for this event.",
    tags=TAGS_REGISTRATION,
    responses={200: ParticipantSerializer(many=True)},
)

REGISTRATION_SCHEMAS = {
    "participants": list_participants,
}
