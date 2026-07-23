package env

import (
	consts "your.module/cue/config:consts"
)

"""
POSTGRES_DB=\(consts.POSTGRES_E2E_DB)
POSTGRES_USER=\(consts.POSTGRES_USER)
POSTGRES_PASSWORD=\(consts.POSTGRES_PASSWORD)
JWT_SECRET_KEY=\(consts.JWT_SECRET_KEY)
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@\(consts.POSTGRES_DB_SERVICE_NAME):5432/\(consts.POSTGRES_E2E_DB)
ALLOWED_ORIGINS='["localhost"]'
"""
