from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue, Empty
from typing import Optional


class Transport(ABC):
    """
    Hardware-independent communication interface.
    """

    @abstractmethod
    def send(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def receive(
        self,
        timeout: float = 0.0,
    ) -> Optional[bytes]:

        raise NotImplementedError


class MockTransport(Transport):
    """
    In-memory transport for software testing.

    This allows us to test the V2V protocol
    without ESP32/LoRa hardware.
    """

    def __init__(self) -> None:
        self._queue: Queue[bytes] = Queue()

    def send(self, data: bytes) -> None:
        self._queue.put(data)

    def receive(
        self,
        timeout: float = 0.0,
    ) -> Optional[bytes]:

        try:
            return self._queue.get(timeout=timeout)

        except Empty:
            return None


class SerialLineTransport(Transport):
    """
    Serial transport for communicating with ESP32.

    Requires:

        pip install pyserial

    The ESP32 should provide one complete
    application message per line.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 0.1,
    ):

        try:
            import serial

        except ImportError as exc:

            raise RuntimeError(
                "pyserial is required. "
                "Install using: pip install pyserial"
            ) from exc

        self._serial = serial.Serial(
            port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def send(self, data: bytes) -> None:

        self._serial.write(data)

    def receive(
        self,
        timeout: float = 0.0,
    ) -> Optional[bytes]:

        if self._serial.in_waiting <= 0:
            return None

        line = self._serial.readline()

        return line if line else None

    def close(self) -> None:

        self._serial.close()