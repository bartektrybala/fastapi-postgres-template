package env

import (
	consts "your.module/cue/config:consts"
)

"""
DATABASE_URL=postgresql://\(consts.POSTGRES_USER):\(consts.POSTGRES_PASSWORD)@localhost:5432/\(consts.POSTGRES_TEST_DB)
ALLOWED_ORIGINS='["*"]'
JWT_SECRET_KEY=dummy-secret-secret
"""
