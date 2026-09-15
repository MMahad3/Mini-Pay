#!/usr/bin/env bash
set -u

URL="${1:-http://localhost:8080/health}"

if curl --fail --silent --show-error --max-time 5 "$URL" >/dev/null; then
    echo "Health check passed: $URL"
    exit 0
fi

echo "Health check failed: $URL" >&2
exit 1
