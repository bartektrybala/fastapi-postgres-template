package main

import (
	"list"
	compose "your.module/cue/docker:compose_generic"
	consts "your.module/cue/config:consts"
)

services: {
	"\(consts.POSTGRES_DB_SERVICE_NAME)": compose.definitions.services[consts.POSTGRES_DB_SERVICE_NAME] & {
		env_file: consts.ENV_FILE_DOCKER
	}
	"\(consts.MIGRATIONS_SERVICE_NAME)": compose.definitions.services[consts.MIGRATIONS_SERVICE_NAME] & {
		env_file: consts.ENV_FILE_DOCKER
	}
	"\(consts.BACKEND_SERVICE_NAME)": compose.definitions.services[consts.BACKEND_SERVICE_NAME] & {
		env_file: consts.ENV_FILE_DOCKER
	}
	"\(consts.API_GATEWAY_SERVICE_NAME)": compose.definitions.services[consts.API_GATEWAY_SERVICE_NAME] & {
		volumes: list.Concat([
			compose.definitions.services[consts.API_GATEWAY_SERVICE_NAME].volumes,
			["../api_gateway/Caddyfile.dev:\(consts.CADDY_CONF_DESTINATION)"],
		])
	}
}

volumes:  compose.definitions.volumes
networks: compose.definitions.networks
