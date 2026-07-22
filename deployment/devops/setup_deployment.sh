#!/bin/bash

set -e

DOMAIN="your-domain.pl"

if [ -z "$GITHUB_DEPLOY_PAT" ]; then
    echo "--- ERROR: GITHUB_DEPLOY_PAT environment variable is not set. ---"
    echo "--- Please export the variable and run the script again. ---"
    exit 1
fi

ssh root@$DOMAIN "bash -s '$GITHUB_DEPLOY_PAT'" << 'EOF'
    set -e

    GITHUB_DEPLOY_PAT="$1"

    # --- [Remote] System Configuration ---
    hostnamectl set-hostname "your-domain"

    echo "--- [Remote] Checking Docker installation... ---"
    if ! command -v docker &> /dev/null; then
        echo "Docker not found. Installing..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh ./get-docker.sh
        rm get-docker.sh
        echo "--- [Remote] Docker installed successfully. ---"
    else
        echo "--- [Remote] Docker is already installed. Skipping. ---"
    fi

    echo "--- [Remote] Installing packages... ---"
    apt-get update
    apt-get install -y git just

    ADMIN_USER_1="bartek"
    APP_USER="docker_runner"

    ADMIN_USER_1_SSH_PUBLIC_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHTfpFbaM0f9Y29u75AbiI3kgZz7864c8iXI7hp7T/Kt bartektrybalaa@gmail.com"
    APP_USER_SSH_PUBLIC_KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAKEMS0z+ZMXSaWec2nYi52CI7aDx832oCDrLJHy12eg docker_runner"

    setup_user() {
        local username=$1
        local public_key=$2
        local is_admin=$3

        if id "$username" &>/dev/null; then
            echo "User '$username' already exists. Skipping creation."
        else
            useradd -m -s /bin/bash "$username"
            echo "User '$username' created."
        fi

        if [ "$is_admin" = true ]; then
            usermod -aG sudo,docker "$username"
        else
            usermod -aG docker "$username"
        fi

        local ssh_dir="/home/$username/.ssh"
        local auth_keys_file="$ssh_dir/authorized_keys"

        mkdir -p "$ssh_dir"
        echo "$public_key" > "$auth_keys_file"
        echo "SSH public key added for user '$username'."

        chown -R "$username:$username" "$ssh_dir"
        chmod 700 "$ssh_dir"
        chmod 600 "$auth_keys_file"
        echo "Permissions set for '$ssh_dir' and '$auth_keys_file'."
    }

    setup_user "$ADMIN_USER_1" "$ADMIN_USER_1_SSH_PUBLIC_KEY" true
    setup_user "$APP_USER" "$APP_USER_SSH_PUBLIC_KEY" false

    # --- Application Repository Setup ---
    REPO_DIR="/home/$APP_USER/second-hand-swag"
    sudo -u "$APP_USER" -H bash -c "rm -r $REPO_DIR"
    sudo -u "$APP_USER" -H bash -c "git clone https://${GITHUB_DEPLOY_PAT}@github.com/bartektrybala/second-hand-swag '$REPO_DIR'"
    echo "--- [Remote] Repository cloned successfully. ---"

    echo "--- [Remote] Running Certbot for initial SSL certificate generation... ---"
    sudo -u "$APP_USER" -H bash -c "cd '$REPO_DIR' && docker compose --file docker-compose/docker-compose-production.yaml up --remove-orphans certbot"

    echo "--- [Remote] Setting up Certbot renewal cron job... ---"
    SOURCE_CRON_FILE="$REPO_DIR/deployment/devops/certbot-renew.cron.d"
    DEST_CRON_FILE="/etc/cron.d/certbot-renew"
    cp "$SOURCE_CRON_FILE" "$DEST_CRON_FILE" && chmod 0644 "$DEST_CRON_FILE"

EOF

echo "--- Script finished. ---"
