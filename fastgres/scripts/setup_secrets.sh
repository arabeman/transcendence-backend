#!/bin/bash

# Define paths
SECRETS_DIR="./secrets"
ENV_FILE="./.env"

# Create secrets directory if it doesn't exist
mkdir -p "$SECRETS_DIR"

# Function to generate a random password : base 64 characters (letters, numbers, operators), 24 bytes, 
# translate delete complement (everything except these characters) => strips symbols base64 has
# points to head of file and  limits the length to 20
generate_password()
{
	openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 20
}

# 1. Generate Postgres Password Secret
if [ ! -f "$SECRETS_DIR/postgres_password" ]; then
	echo "Generating Postgres password..."
	generate_password > "$SECRETS_DIR/postgres_password"
else
	echo "Postgres password already exists."
fi


# 2. Generate pgAdmin Password Secret
if [ ! -f "$SECRETS_DIR/pgadmin_password" ]; then
	echo "Generateing pgAdmin password..."
	generate_password > "$SECRETS_DIR/pgadmin_password"
else
	echo "pgAdmin password already exists."
fi

# 3 Generate .env file for non-sensitive data
if [ ! -f "$ENV_FILE" ]; then
	echo "Creating .env file ..."
	cat <<EOF > "$ENV_FILE"
# Project Configuration
PROJECT_NAME=fastgres

# Postgres Configuration
POSTGRES_USER=postgres
POSTGRES_DB=app_db
POSTGRES_PORT=5433

# pgAdmin Configuration
PGADMIN_EMAIL=huhu@admin.com
PGADMIN_PORT=5050
EOF
else
	echo ".env file already exists."
fi

echo "Setup complete! Secrets are in $SECRETS_DIR and config is in $ENV_FILE"