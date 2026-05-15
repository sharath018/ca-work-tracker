"""
Version management utility for build scripts.
"""

import re
from pathlib import Path


def read_version(version_file="version.txt"):
    """Read version from version.txt"""
    try:
        with open(version_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def update_version(new_version, version_file="version.txt"):
    """Update version in version.txt"""
    with open(version_file, 'w') as f:
        f.write(new_version)
    print(f"Version updated to {new_version}")


def bump_patch(current_version):
    """Bump patch version (1.0.0 -> 1.0.1)"""
    parts = current_version.split('.')
    parts[2] = str(int(parts[2]) + 1)
    return '.'.join(parts)


def bump_minor(current_version):
    """Bump minor version (1.0.0 -> 1.1.0)"""
    parts = current_version.split('.')
    parts[1] = str(int(parts[1]) + 1)
    parts[2] = "0"
    return '.'.join(parts)


def bump_major(current_version):
    """Bump major version (1.0.0 -> 2.0.0)"""
    parts = current_version.split('.')
    parts[0] = str(int(parts[0]) + 1)
    parts[1] = "0"
    parts[2] = "0"
    return '.'.join(parts)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        current = read_version()
        print(f"Current version: {current}")
        print("\nUsage: python version.py <major|minor|patch>")
        sys.exit(0)
    
    action = sys.argv[1].lower()
    current_version = read_version()
    
    if action == "major":
        new_version = bump_major(current_version)
    elif action == "minor":
        new_version = bump_minor(current_version)
    elif action == "patch":
        new_version = bump_patch(current_version)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
    
    update_version(new_version)
