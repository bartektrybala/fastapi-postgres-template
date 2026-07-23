package consts

TEST:        "test"
DEVELOPMENT: "development"
DOCKER:      "docker"
PRODUCTION:  "production"

ENV_DIR:              "../src/env/"
ENV_FILE_TEST:        "\(ENV_DIR).env.\(TEST)"
ENV_FILE_DEVELOPMENT: "\(ENV_DIR).env.\(DEVELOPMENT)"
ENV_FILE_DOCKER:      "\(ENV_DIR).env.\(DOCKER)"
ENV_FILE_PRODUCTION:  "\(ENV_DIR).env.\(PRODUCTION)"

POSTGRES_DB_SERVICE_NAME: "db"
POSTGRES_LOCAL_DB:        "shs-local"
POSTGRES_TEST_DB:         "testing"
POSTGRES_USER:            "postgres"
POSTGRES_PASSWORD:        "password"
POSTGRES_PORT:            5432

POSTGRES_DBDATA_VOLUME_NAME:   "dbdata"
POSTGRES_SERVICE_VOLUME_MOUNT: "\(POSTGRES_DBDATA_VOLUME_NAME):/var/lib/postgresql/data"
POSTGRES_DB_NETWORK_NAME:      "db_network"

MIGRATIONS_SERVICE_NAME: "shs-migrations"
BACKEND_SERVICE_NAME:    "shs-backend"
BACKEND_SERVICE_PORT:    8000
BACKEND_NETWORK_NAME:    "backend_network"

API_GATEWAY_SERVICE_NAME: "api-gateway"
API_GATEWAY_HTTP_PORT:    80
API_GATEWAY_HTTPS_PORT:   443
NGINX_CONF_DESTINATION:   "/etc/nginx/nginx.conf:ro"

DOMAIN_DNS: "your-domain.pl"
SENTRY_DSN: "https://your-sentry-dns.ingest.de.sentry.io/your-sentry-dns"

CERTBOT_SERVICE_NAME: "certbot"
CERTBOT_VOLUME_NAME:  "certbot_volume"
CERTBOT_VOLUME_MOUNT: "\(CERTBOT_VOLUME_NAME):/etc/letsencrypt"

JWT_SECRET_KEY: "tmp-super-super-secret-value-secret-value-secret-value-value-secret-value"
