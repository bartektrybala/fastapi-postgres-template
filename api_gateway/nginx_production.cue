import (
	consts "your.module/cue/config:consts"
)

"""
events {}
http {
    include       mime.types;
    server {
        listen 443 ssl;
        server_name \(consts.DOMAIN_DNS) www.\(consts.DOMAIN_DNS);
        ssl_certificate     /etc/letsencrypt/live/\(consts.DOMAIN_DNS)/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/\(consts.DOMAIN_DNS)/privkey.pem;

        location / {
            proxy_pass http://\(consts.BACKEND_SERVICE_NAME):\(consts.BACKEND_SERVICE_PORT);
        }
    }
    server {
        listen 80;
        server_name \(consts.DOMAIN_DNS) www.\(consts.DOMAIN_DNS);
        return 301 https://\(consts.DOMAIN_DNS)$request_uri;
    }
}
"""
