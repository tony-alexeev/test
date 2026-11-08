#!/bin/sh
set -eu

image=$1
expected_sha=$2
container=$(docker run -d --rm -p 127.0.0.1::8000 "$image")
trap 'docker rm -f "$container" >/dev/null 2>&1 || true' EXIT HUP INT TERM
port=$(docker port "$container" 8000/tcp)
base="http://127.0.0.1:${port##*:}"

ready=0
for attempt in 1 2 3 4 5 6 7 8 9 10; do
    if curl --silent --fail "$base/healthz" | python3 -c 'import json,sys; assert json.load(sys.stdin) == {"status": "ok"}' 2>/dev/null; then
        ready=1
        break
    fi
    sleep 1
done
test "$ready" -eq 1

curl --silent --show-error --fail "$base/version" |
    python3 -c 'import json,sys; assert json.load(sys.stdin) == {"sha": sys.argv[1]}' "$expected_sha"
curl --silent --show-error --fail "$base/access?owner_id=alice&requester_id=alice" |
    python3 -c 'import json,sys; assert json.load(sys.stdin) == {"allowed": True}'
status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$base/access?owner_id=alice&requester_id=bob")
test "$status" = 403
status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$base/access?owner_id=alice")
test "$status" = 403
printf 'Smoke passed for %s at %s\n' "$image" "$expected_sha"
