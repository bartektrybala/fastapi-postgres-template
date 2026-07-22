package compose_generic

import consts "your.module/cue/config:consts"

#_healthcheck: {
	test:         string
	interval:     "3s"
	timeout:      "5s"
	retries:      10
	start_period: "2s"
}

#_python_http_healthcheck: #_healthcheck & {
	_url: string
	test: "python -c 'import urllib.request; urllib.request.urlopen(\(_url))'"
}

definitions: {
	services: {
		"\(consts.POSTGRES_DB_SERVICE_NAME)": {
			image:   "postgres:17"
			restart: "unless-stopped"
			healthcheck: #_healthcheck & {test: "pg_isready -U postgres"}
			env_file: string
			networks: [consts.POSTGRES_DB_NETWORK_NAME]
			volumes: [consts.POSTGRES_SERVICE_VOLUME_MOUNT]
		}
		"\(consts.MIGRATIONS_SERVICE_NAME)": {
			build: {
				context:    "../"
				dockerfile: "Dockerfile"
			}
			depends_on: {
				"\(consts.POSTGRES_DB_SERVICE_NAME)": {
					condition: "service_healthy"
				}
			}
			command:  "sh -c 'cd src/infrastructure/sqlalchemy && uv run alembic upgrade head'"
			env_file: string
			networks: [consts.POSTGRES_DB_NETWORK_NAME]
			volumes: [consts.POSTGRES_SERVICE_VOLUME_MOUNT]
		}
		"\(consts.BACKEND_SERVICE_NAME)": {
			build: {
				context:    "../"
				dockerfile: "Dockerfile"
			}
			env_file: string
			networks: [consts.POSTGRES_DB_NETWORK_NAME, consts.BACKEND_NETWORK_NAME]
			healthcheck: #_python_http_healthcheck & {
				_url: "\"http://\(consts.BACKEND_SERVICE_NAME):\(consts.BACKEND_SERVICE_PORT)/health\""
			}
			depends_on: {
				"\(consts.MIGRATIONS_SERVICE_NAME)": {
					condition: "service_completed_successfully"
				}
			}
		}
		"\(consts.API_GATEWAY_SERVICE_NAME)": {
			image:   "nginx:latest"
			restart: "unless-stopped"
			ports: [
				"\(consts.API_GATEWAY_HTTP_PORT):\(consts.API_GATEWAY_HTTP_PORT)",
				"\(consts.API_GATEWAY_HTTPS_PORT):\(consts.API_GATEWAY_HTTPS_PORT)",
			]
			networks: [consts.BACKEND_NETWORK_NAME]
			volumes: [...string]
			depends_on: {
				"\(consts.BACKEND_SERVICE_NAME)": {
					condition: "service_healthy"
				}
			}
		}
		"\(consts.CERTBOT_SERVICE_NAME)": {
			image:          "certbot/certbot"
			container_name: "certbot"
			profiles: ["certbot"]
			restart: "no"
			ports: ["80:80"]
			volumes: [consts.CERTBOT_VOLUME_MOUNT]
			command: "certonly --standalone --email bartektrybalaa@gmail.com --agree-tos --preferred-challenges http -d \(consts.DOMAIN_DNS)"
		}
	}

	volumes: {
		"\(consts.POSTGRES_DBDATA_VOLUME_NAME)": driver: "local"
		"\(consts.CERTBOT_VOLUME_NAME)": driver:         "local"
	}

	networks: {
		"\(consts.POSTGRES_DB_NETWORK_NAME)": driver: "bridge"
		"\(consts.BACKEND_NETWORK_NAME)": driver:     "bridge"
	}
}
