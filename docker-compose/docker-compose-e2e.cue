package main

import (
	compose "your.module/cue/docker:compose_generic"
	consts "your.module/cue/config:consts"
)

services: {
	"\(consts.POSTGRES_DB_SERVICE_NAME)": compose.definitions.services[consts.POSTGRES_DB_SERVICE_NAME] & {
		ports: ["\(consts.POSTGRES_PORT):\(consts.POSTGRES_PORT)"]
		env_file: consts.ENV_FILE_E2E
	}
	"\(consts.MIGRATIONS_SERVICE_NAME)": compose.definitions.services[consts.MIGRATIONS_SERVICE_NAME] & {
		env_file: consts.ENV_FILE_E2E
	}
	"\(consts.BACKEND_SERVICE_NAME)": compose.definitions.services[consts.BACKEND_SERVICE_NAME] & {
		env_file: consts.ENV_FILE_E2E
	}
	"\(consts.API_GATEWAY_SERVICE_NAME)": compose.definitions.services[consts.API_GATEWAY_SERVICE_NAME] & {
		volumes: [
			"../api_gateway/nginx.conf:\(consts.NGINX_CONF_DESTINATION)",
		]
	}
}

volumes: {
	"\(consts.POSTGRES_DBDATA_VOLUME_NAME)": compose.definitions.volumes.dbdata
}

networks: {
	"\(consts.POSTGRES_DB_NETWORK_NAME)": compose.definitions.networks.db_network
	"\(consts.BACKEND_NETWORK_NAME)":     compose.definitions.networks.backend_network
}
