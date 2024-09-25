#!/bin/bash

# Exit on error
set -e

# Ensure a version bump type is provided (patch, minor, or major)
if [ -z "$1" ]; then
  echo "Usage: ./release [patch|minor|major]"
  exit 1
fi

# Bump version using Poetry
new_version=$(poetry version "$1" | awk '{print $NF}')
echo "New version: $new_version"

# Create a Git tag (e.g., v1.2.3)
tag="v$new_version"
git tag "$tag"
echo "Created tag: $tag"

# Commit the version change
git add pyproject.toml
git commit -m "Bump version to $new_version"

# Push the changes and the tag to GitHub
git push origin main
git push origin "$tag"

echo "Pushed changes and tag to GitHub. Release workflow should trigger now."

