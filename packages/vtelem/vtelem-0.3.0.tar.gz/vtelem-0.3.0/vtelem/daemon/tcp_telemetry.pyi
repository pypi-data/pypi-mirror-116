import socketserver
from typing import Any, Tuple
from vtelem.classes.stream_writer import QueueClientManager as QueueClientManager, StreamWriter as StreamWriter
from vtelem.daemon import DaemonBase as DaemonBase
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

LOG: Any

class TcpTelemetryHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None: ...

class TcpTelemetryDaemon(QueueClientManager, DaemonBase):
    server: Any
    client_sems: Any
    def __init__(self, name: str, writer: StreamWriter, env: TelemetryEnvironment, address: Tuple[str, int] = ..., time_keeper: Any = ...) -> None: ...
    @property
    def address(self) -> Tuple[str, int]: ...
    def run(self, *_, **__) -> None: ...
