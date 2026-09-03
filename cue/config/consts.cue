package consts

TEST:        "test"
E2E:         "e2e"
DEVELOPMENT: "development"
DOCKER:      "docker"
PRODUCTION:  "production"

ENV_DIR:              "../src/env/"
ENV_FILE_TEST:        "\(ENV_DIR).env.\(TEST)"
ENV_FILE_DEVELOPMENT: "\(ENV_DIR).env.\(DEVELOPMENT)"
ENV_FILE_DOCKER:      "\(ENV_DIR).env.\(DOCKER)"
ENV_FILE_E2E:         "\(ENV_DIR).env.\(E2E)"
ENV_FILE_PRODUCTION:  "\(ENV_DIR).env.\(PRODUCTION)"

POSTGRES_DB_SERVICE_NAME: "db"
POSTGRES_LOCAL_DB:        "local"
POSTGRES_E2E_DB:          "e2e_testing"
POSTGRES_TEST_DB:         "testing"
POSTGRES_USER:            "postgres"
POSTGRES_PASSWORD:        "password"
POSTGRES_PORT:            5432

POSTGRES_DBDATA_VOLUME_NAME:   "dbdata"
POSTGRES_SERVICE_VOLUME_MOUNT: "\(POSTGRES_DBDATA_VOLUME_NAME):/var/lib/postgresql/data"
POSTGRES_DB_NETWORK_NAME:      "db_network"

MIGRATIONS_SERVICE_NAME: "migrations"
BACKEND_SERVICE_NAME:    "backend"
BACKEND_SERVICE_PORT:    8000
BACKEND_NETWORK_NAME:    "backend_network"

API_GATEWAY_SERVICE_NAME:  "caddy"
API_GATEWAY_HTTP_PORT:     80
API_GATEWAY_HTTPS_PORT:    443
CADDY_CONF_DESTINATION:    "/etc/caddy/Caddyfile:ro"
CADDY_DATA_VOLUME:         "caddy_data"
CADDY_CONFIG_VOLUME:       "caddy_config"
CADDY_DATA_VOLUME_MOUNT:   "\(CADDY_DATA_VOLUME):/data"
CADDY_CONFIG_VOLUME_MOUNT: "\(CADDY_CONFIG_VOLUME):/config"

DOMAIN_DNS: "your-domain.pl"
SENTRY_DSN: "https://your-sentry-dns.ingest.de.sentry.io/your-sentry-dns"

JWT_SECRET_KEY: "tmp-super-super-secret-value-secret-value-secret-value-value-secret-value"
