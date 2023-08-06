from queue import Queue
from typing import Any, Optional, Tuple
from vtelem.classes.stream_writer import QueueClientManager as QueueClientManager, StreamWriter as StreamWriter
from vtelem.daemon.websocket import WebsocketDaemon as WebsocketDaemon
from vtelem.frame.channel import ChannelFrame as ChannelFrame
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

def queue_get(queue: Queue, timeout: int = ...) -> Optional[Any]: ...

class WebsocketTelemetryDaemon(QueueClientManager, WebsocketDaemon):
    def __init__(self, name: str, writer: StreamWriter, address: Tuple[str, int] = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
