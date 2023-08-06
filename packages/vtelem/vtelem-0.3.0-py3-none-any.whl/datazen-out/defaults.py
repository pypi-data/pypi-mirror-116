# =====================================
# generator=datazen
# version=1.7.8
# hash=1977d990a0139e3fcca938d45a595980
# =====================================
"""
vtelem - Class defaults.
"""

# built-in
from typing import Tuple, Any

# internal
from vtelem.enums.primitive import Primitive

ENUM_PRIM = Primitive.UINT8
TIMESTAMP_PRIM = Primitive.UINT64
METRIC_PRIM = Primitive.UINT32
COUNT_PRIM = Primitive.UINT32
ID_PRIM = Primitive.UINT16

EventType = Tuple[Any, float]

LOG_PERIOD: float = 0.25
