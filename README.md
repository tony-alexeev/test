# Private report access

A report is private to its owner. A requester can read the report only when
`requester_id` and `owner_id` are the same nonempty account ID. Anonymous
requesters and other accounts must be denied.

## CA-06 fixture

This HTTP service uses synthetic account IDs. It calls the existing
`can_view_report` rule. It has no accounts, stored reports, or authentication.
Do not use it to protect real data.

The proposed CA-06 behavior is:

- **CA06-01:** Given matching, nonempty IDs, when a client requests
  `/access`, the service returns HTTP 200 and `{"allowed":true}`.
- **CA06-02:** Given different IDs or no requester ID, the service returns
  HTTP 403 and `{"allowed":false}`. A missing owner ID returns HTTP 400.
- **CA06-03:** Given a running container, `/healthz` returns HTTP 200 and
  `/version` returns the exact SHA used to build that container.
- **CA06-04:** Given a PR, CI runs unit tests and smokes the image it builds.
  It does not access GitHub secrets or publish an image.
- **CA06-05:** Given a push to `main` after a merge, CI runs the same checks.
  Only after they pass does it load that checked image and push one SHA tag to
  GHCR. It writes the full digest reference and main SHA to the job summary.
- **CA06-06 (proposed):** Given repeated identity parameters in an `/access`
  request, the service returns HTTP 400 instead of selecting one value.

### Run locally

Use Python 3.12 and Docker. No external service is needed.

```sh
python3 -m unittest discover -v
sha=$(git rev-parse HEAD)
docker build --build-arg APP_VERSION="$sha" -t "ca06-checked:$sha" .
sh scripts/smoke.sh "ca06-checked:$sha" "$sha"
```

For a direct HTTP check, start the container with
`docker run --rm -p 127.0.0.1:8000:8000 "ca06-checked:$sha"`. Then request
`http://127.0.0.1:8000/healthz`,
`http://127.0.0.1:8000/version`, or
`http://127.0.0.1:8000/access?owner_id=alice&requester_id=alice`.

### Check a PR and a release

The **Test and publish fixture** workflow runs on every PR and on pushes to
`main`. In the PR, check that `verify` passed. It runs the Python tests,
builds the image with the checked revision SHA, and calls the HTTP endpoints
inside the container.

After a merge, check that both `verify` and `publish` passed for the new
`main` SHA. Open the `publish` job summary. Copy the full
`ghcr.io/tony-alexeev/test@sha256:...` reference and the main SHA into the
release record. The SHA tag is `ghcr.io/tony-alexeev/test:sha-<main SHA>`.
The digest reference names the exact published image. A PR has no published
digest. CI does not deploy the image.

On a rerun, the publish job checks an existing SHA tag. It records its digest
without a second push only if the pulled image matches the checked image.
It stops on a registry error or a different image. Inspect the job log before
retrying a failed release.
