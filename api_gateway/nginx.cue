import (
	consts "your.module/cue/config:consts"
)

"""
events {}
http {
    include       mime.types;
    server {
        listen 80;
        location / {
            proxy_pass http://\(consts.BACKEND_SERVICE_NAME):\(consts.BACKEND_SERVICE_PORT);
        }
    }
}
"""
