from __future__ import annotations

import json

from communication.message_schema import V2VMessage


def encode_message(
    message: V2VMessage
) -> str:
    """
    Convert a V2VMessage into a JSON string.
    """

    return json.dumps(
        message.to_dict(),
        separators=(",", ":")
    )


def encode_bytes(
    message: V2VMessage
) -> bytes:
    """
    Convert a V2VMessage into bytes.

    This will eventually be suitable for
    transmission through LoRa.
    """

    return (
        encode_message(message) + "\n"
    ).encode("utf-8")