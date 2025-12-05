from drf_spectacular.utils import extend_schema

TAGS_EVENTS = ["Events"]

list_events = extend_schema(
    summary="List all events",
    description="Get a paginated list of all events with filtering.",
    tags=TAGS_EVENTS,
)

retrieve_event = extend_schema(
    summary="Get event details",
    description="Get detailed information about a specific event.",
    tags=TAGS_EVENTS,
)

create_event = extend_schema(
    summary="Create a new event",
    description="Create a new event. Requires authentication.",
    tags=TAGS_EVENTS,
)

update_event = extend_schema(
    summary="Update an event",
    description="Update an event. Only the organizer can update.",
    tags=TAGS_EVENTS,
)

partial_update_event = extend_schema(
    summary="Partially update an event",
    description="Partially update an event. Only the organizer can update.",
    tags=TAGS_EVENTS,
)

destroy_event = extend_schema(
    summary="Delete an event",
    description="Delete an event. Only the organizer can delete.",
    tags=TAGS_EVENTS,
)

EVENT_SCHEMAS = {
    "list": list_events,
    "retrieve": retrieve_event,
    "create": create_event,
    "update": update_event,
    "partial_update": partial_update_event,
    "destroy": destroy_event,
}
