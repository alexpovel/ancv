import structlog
from structlog.processors import JSONRenderer, TimeStamper, add_log_level

structlog.configure(
    processors=[  # https://www.structlog.org/en/stable/api.html#procs
        TimeStamper(fmt="iso", utc=True, key="ts"),
        add_log_level,
        JSONRenderer(sort_keys=True),
    ]
)

LOGGER = structlog.get_logger()
