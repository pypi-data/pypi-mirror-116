from typing import Any
from vtelem.daemon.command_queue import CommandQueueDaemon as CommandQueueDaemon
from vtelem.daemon.telemetry import TelemetryDaemon as TelemetryDaemon

def register_http_handlers(server: Any, telem: TelemetryDaemon, cmd: CommandQueueDaemon) -> None: ...
