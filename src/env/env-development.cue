package env

import (
	consts "your.module/cue/config:consts"
)

"""
POSTGRES_DB=\(consts.POSTGRES_LOCAL_DB)
POSTGRES_USER=\(consts.POSTGRES_USER)
POSTGRES_PASSWORD=\(consts.POSTGRES_PASSWORD)
JWT_SECRET_KEY=\(consts.JWT_SECRET_KEY)
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@localhost:5432/\(consts.POSTGRES_LOCAL_DB)
ALLOWED_ORIGINS='["*"]'
"""
