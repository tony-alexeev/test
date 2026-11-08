#!/usr/bin/env bash
set -euo pipefail

repo=${GITHUB_REPOSITORY,,}
local_image="ca06-checked:$GITHUB_SHA"
tagged_image="ghcr.io/$repo:sha-$GITHUB_SHA"

printf '%s' "$GH_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
registry_token=$(
  curl --fail --silent --show-error --get \
    --user "$GITHUB_ACTOR:$GH_TOKEN" \
    --data-urlencode "scope=repository:$repo:pull,push" \
    --data-urlencode "service=ghcr.io" \
    https://ghcr.io/token |
    python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])'
)
status=$(
  curl --silent --show-error --head --output manifest.headers \
    --write-out '%{http_code}' \
    --header "Authorization: Bearer $registry_token" \
    --header 'Accept: application/vnd.oci.image.manifest.v1+json, application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.v2+json, application/vnd.docker.distribution.manifest.list.v2+json' \
    "https://ghcr.io/v2/$repo/manifests/sha-$GITHUB_SHA"
)

case "$status" in
  200)
    digest=$(
      python3 -c 'import re,sys; values=re.findall(r"^docker-content-digest:\s*(sha256:[0-9a-f]{64})\s*$", open(sys.argv[1]).read(), re.I|re.M); assert values; print(values[-1])' manifest.headers
    )
    echo "Existing SHA tag found; checking its image ID."
    ;;
  404)
    docker tag "$local_image" "$tagged_image"
    docker push "$tagged_image" | tee push.log
    digest=$(sed -n 's/.*digest: \(sha256:[0-9a-f]*\).*/\1/p' push.log | tail -n 1)
    test "${#digest}" -eq 71
    ;;
  *)
    echo "Registry lookup failed with HTTP $status; no push was attempted." >&2
    exit 1
    ;;
esac

reference="ghcr.io/$repo@$digest"
docker pull "$reference"
checked_id=$(docker image inspect --format '{{.Id}}' "$local_image")
published_id=$(docker image inspect --format '{{.Id}}' "$reference")
if [[ "$checked_id" != "$published_id" ]]; then
  echo "Published image differs from the checked image." >&2
  exit 1
fi

printf 'main SHA: `%s`\nImage: `%s`\nDigest reference: `%s`\nChecked image ID: `%s`\n' \
  "$GITHUB_SHA" "$tagged_image" "$reference" "$checked_id" >> "$GITHUB_STEP_SUMMARY"
printf '%s\n' "$reference"
