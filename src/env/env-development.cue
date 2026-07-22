package env

import (
	consts "your.module/cue/config:consts"
)

"""
POSTGRES_DB=\(consts.POSTGRES_LOCAL_DB)
POSTGRES_USER=\(consts.POSTGRES_USER)
POSTGRES_PASSWORD=\(consts.POSTGRES_PASSWORD)
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@localhost:5432/\(consts.POSTGRES_LOCAL_DB)
ALLOWED_ORIGINS='["*"]'
"""
