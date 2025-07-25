#!/bin/bash

set -Eeuo pipefail

# Check that there is exactly one argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <message>"
    exit 1
fi

MESSAGE="$1"

echo -e "$MESSAGE"

if [ "${SILENT:-false}" != true ]; then
    VOICE=${VOICE:-Serena (Premium)}
    say --voice "${VOICE}" "$MESSAGE" &
fi

curl --silent \
    --output /dev/null \
    --form-string "token=$PUSHOVER_APP_TOKEN" \
    --form-string "user=$PUSHOVER_USER_KEY" \
    --form-string "message=$MESSAGE" \
    https://api.pushover.net/1/messages.json