#!/bin/bash

gitlab-runner register \
  --non-interactive \
  --url "http://gitlab-ce:80" \
  --token "${GITLAB_RUNNER_TOKEN}"\
  --executor "docker" \
  --docker-image "alpine:latest" \
  --description "gitlab-runner for ServeHub" \
  --docker-privileged="true" \
  --docker-network-mode "gitlab-net"