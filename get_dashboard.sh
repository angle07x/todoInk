#!/bin/sh
# Get the directory where this .sh script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Load variables from .env using POSIX '.'
if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a
    . "$SCRIPT_DIR/.env"
    set +a
fi
IMG_PATH="/tmp/dashboard.png"

wget -q -O "$IMG_PATH" "$URL"

if [ $? -eq 0 ]; then
    # Update this line to use the full path to fbink
    /mnt/us/extensions/dashboard/bin/fbink -c -f -i "$IMG_PATH"
else
    /usr/bin/eips "Failed to fetch dashboard."
fi