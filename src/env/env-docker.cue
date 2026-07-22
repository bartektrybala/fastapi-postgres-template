package env

import (
	consts "your.module/cue/config:consts"
)

"""
POSTGRES_DB=\(consts.POSTGRES_LOCAL_DB)
POSTGRES_USER=\(consts.POSTGRES_USER)
POSTGRES_PASSWORD=\(consts.POSTGRES_PASSWORD)
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@\(consts.POSTGRES_DB_SERVICE_NAME):5432/\(consts.POSTGRES_LOCAL_DB)
BROWSER_WS_ENDPOINT=ws://\(consts.BROWSER_SERVICE_NAME):\(consts.BROWSER_SERVICE_PORT)/
ALLOWED_ORIGINS='["localhost"]'
X_API_KEY_HASH=\(consts.X_API_KEY_HASH_DUMMY)
"""
