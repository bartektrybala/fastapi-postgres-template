import (
	consts "your.module/cue/config:consts"
)

"""
\(consts.DOMAIN_DNS) {
    handle {
        reverse_proxy \(consts.BACKEND_SERVICE_NAME):\(consts.BACKEND_SERVICE_PORT)
    }
}
"""
