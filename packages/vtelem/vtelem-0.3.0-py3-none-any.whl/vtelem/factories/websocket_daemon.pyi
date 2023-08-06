from typing import Tuple
from vtelem.classes.time_keeper import TimeKeeper as TimeKeeper
from vtelem.daemon.command_queue import CommandQueueDaemon as CommandQueueDaemon
from vtelem.daemon.websocket import WebsocketDaemon as WebsocketDaemon
from vtelem.telemetry.environment import TelemetryEnvironment as TelemetryEnvironment

def commandable_websocket_daemon(name: str, daemon: CommandQueueDaemon, address: Tuple[str, int] = ..., env: TelemetryEnvironment = ..., keeper: TimeKeeper = ...) -> WebsocketDaemon: ...
