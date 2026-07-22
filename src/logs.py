import logging
from dataclasses import dataclass


# solution adapted from https://joshdimella.com/blog/filtering-fastapi-logs
@dataclass
class EndpointFilter(logging.Filter):
    excluded_endpoints: list[str]

    def filter(self, record: logging.LogRecord) -> bool:
        return not any(
            endpoint in record.getMessage() for endpoint in self.excluded_endpoints
        )
