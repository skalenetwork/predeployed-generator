#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."
./scripts/generate_package_version.py > version.txt
./scripts/prepare_artifacts.sh
python3 -m build
