import (
	consts "your.module/cue/config:consts"
)

"""
:80 {
    handle {
        reverse_proxy \(consts.BACKEND_SERVICE_NAME):\(consts.BACKEND_SERVICE_PORT)
    }
}
"""
