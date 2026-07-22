package env

import (
	consts "your.module/cue/config:consts"
)

"""
POSTGRES_DB=\(consts.POSTGRES_LOCAL_DB)
POSTGRES_USER=\(consts.POSTGRES_USER)
POSTGRES_PASSWORD=\(consts.POSTGRES_PASSWORD)
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@\(consts.POSTGRES_DB_SERVICE_NAME):5432/\(consts.POSTGRES_LOCAL_DB)
ALLOWED_ORIGINS='["\(consts.DOMAIN_DNS)"]'
SENTRY_DSN=\(consts.SENTRY_DSN)
"""
