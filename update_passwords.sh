#!/bin/bash

# Configuration variables - modify as needed
DB_NAME="doccano"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
# DB_PASSWORD="" # Uncomment and set if needed

# Password hash to set for all users (escaped $ with \$)
PASSWORD_HASH="pbkdf2_sha256\$600000\$Oy4u275M8Y3Y4PMNzZ7P5q\$973rwmGKbw5vL5EQoYUzYVvZV7GmveHqGhI9lCf3iBs="

# Function to display usage information
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -d DB_NAME   Database name (default: $DB_NAME)"
    echo "  -u DB_USER   Database user (default: $DB_USER)"
    echo "  -h DB_HOST   Database host (default: $DB_HOST)"
    echo "  -p DB_PORT   Database port (default: $DB_PORT)"
    echo "  -w DB_PASS   Database password (if required)"
    echo "  -? --help    Show this help"
    exit 1
}

# Process command line arguments
while getopts "d:u:h:p:w:?" opt; do
    case $opt in
        d) DB_NAME=$OPTARG ;;
        u) DB_USER=$OPTARG ;;
        h) DB_HOST=$OPTARG ;;
        p) DB_PORT=$OPTARG ;;
        w) DB_PASSWORD=$OPTARG ;;
        \?|*) usage ;;
    esac
done

# Build the psql connection
if [ -n "$DB_PASSWORD" ]; then
    export PGPASSWORD="$DB_PASSWORD"
    CONNECTION_STRING="-h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
else
    CONNECTION_STRING="-h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"
fi

# Execute the SQL command
echo "Updating all passwords in the auth_user table..."
psql $CONNECTION_STRING -c "UPDATE auth_user SET password = '$PASSWORD_HASH';"

# Check if command was successful
if [ $? -eq 0 ]; then
    echo "Password update completed successfully."
else
    echo "Error: Failed to update passwords."
    exit 1
fi

# Unset password if it was set
if [ -n "$DB_PASSWORD" ]; then
    unset PGPASSWORD
fi
