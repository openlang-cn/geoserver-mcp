#!/bin/bash

# Generated from official installation evidence:
# - https://github.com/openlang-cn/geoserver-mcp/blob/main/deploy/Dockerfile

# Adjust host-mounted data directory permissions for the container runtime user.
if [ -d data ]; then
    chown -R 10001:10001 data
    chmod -R 755 data
fi
