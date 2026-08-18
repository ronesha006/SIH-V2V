from __future__ import annotations

import json

from communication.message_schema import V2VMessage


def decode_message(
    raw: str | bytes
) -> V2VMessage:
    """
    Convert received JSON data back into
    a V2VMessage object.
    """

    if isinstance(raw, bytes):

        raw = raw.decode("utf-8")

    raw = raw.strip()

    if not raw:

        raise ValueError(
            "Received empty message"
        )

    try:

        data = json.loads(raw)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Invalid JSON message: {exc}"
        ) from exc

    return V2VMessage.from_dict(data)