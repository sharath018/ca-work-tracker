"""GitHub-based version checking for CA Work Tracker."""

import urllib.request
import urllib.error
import json
import logging
from packaging import version as pkg_version
from datetime import datetime, timedelta

logger = logging.getLogger("CAWorkTracker")

REPO_OWNER = "sharath018"
REPO_NAME = "ca-work-tracker"
GITHUB_API_LATEST = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
GITHUB_API_RELEASES = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases?per_page=1"
GITHUB_API_TAGS = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/tags?per_page=1"
GITHUB_RELEASES_PAGE = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases"


class VersionChecker:
    """Check for new versions from GitHub releases."""

    def __init__(self, current_version, cache_hours=24):
        """
        Initialize version checker.

        Args:
            current_version: Current app version string (e.g., "1.0.0")
            cache_hours: Hours to cache version check results
        """
        self.current_version = current_version
        self.cache_hours = cache_hours
        self.last_check_time = None
        self.cached_latest_version = None
        self.cached_release_url = None

    def _fetch_json(self, url, timeout=5):
        """Fetch and parse JSON from GitHub API."""
        req = urllib.request.Request(url, headers={"User-Agent": "CA Work Tracker"})
        response = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(response.read().decode("utf-8"))

    def _get_release_data(self):
        """Try multiple endpoints to get release info (handles repos with no releases)."""
        try:
            # Try /releases/latest first (most common case)
            data = self._fetch_json(GITHUB_API_LATEST)
            return data, "release"
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            logger.debug("No releases found, trying releases list...")

        try:
            # Fall back to /releases?per_page=1 (list endpoint, works even if no releases)
            data = self._fetch_json(GITHUB_API_RELEASES)
            if isinstance(data, list) and len(data) > 0:
                return data[0], "release"
            logger.debug("No releases found, trying tags list...")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise

        try:
            # Fall back to /tags?per_page=1 (tags endpoint)
            data = self._fetch_json(GITHUB_API_TAGS)
            if isinstance(data, list) and len(data) > 0:
                return data[0], "tag"
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise

        return None, None

    def check_for_updates(self, force=False):
        """
        Check GitHub for the latest release.

        Returns:
            Tuple: (has_update: bool, latest_version: str, release_url: str, error: str or None)
        """
        # Use cache if available and not forced
        if (
            not force
            and self.last_check_time
            and datetime.now() - self.last_check_time < timedelta(hours=self.cache_hours)
        ):
            if self.cached_latest_version:
                try:
                    has_update = pkg_version.parse(
                        self.cached_latest_version
                    ) > pkg_version.parse(self.current_version)
                    return has_update, self.cached_latest_version, self.cached_release_url, None
                except Exception:
                    pass

        try:
            data, data_type = self._get_release_data()

            if not data:
                msg = "No updates available yet."
                logger.info(f"No releases found for {REPO_OWNER}/{REPO_NAME}")
                return False, None, None, msg

            # Extract version from release or tag
            if data_type == "tag":
                latest_version = data.get("name", "").lstrip("v")
                release_url = GITHUB_RELEASES_PAGE
            else:
                latest_version = data.get("tag_name", "").lstrip("v") or data.get("name", "").lstrip("v")
                release_url = data.get("html_url", "") or GITHUB_RELEASES_PAGE

            if not latest_version:
                return False, None, None, "Could not extract version from GitHub"

            # Cache result
            self.last_check_time = datetime.now()
            self.cached_latest_version = latest_version
            self.cached_release_url = release_url

            # Compare versions
            has_update = pkg_version.parse(latest_version) > pkg_version.parse(
                self.current_version
            )

            logger.info(
                f"Version check: current={self.current_version}, latest={latest_version}, "
                f"update_available={has_update}"
            )

            return has_update, latest_version, release_url, None

        except urllib.error.URLError as e:
            logger.warning(f"Failed to check GitHub for updates: {e}")
            return False, None, None, f"Network error: {str(e)}"
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse GitHub response: {e}")
            return False, None, None, f"Parse error: {str(e)}"
        except Exception as e:
            logger.warning(f"Unexpected error checking for updates: {e}")
            return False, None, None, f"Unexpected error: {str(e)}"

    def get_release_notes(self, release_url):
        """
        Extract release notes from release URL.

        Returns:
            str: Release notes or None if unavailable
        """
        try:
            # Convert GitHub web URL to API URL
            api_url = release_url.replace("releases/tag/", "releases/tags/")
            response = urllib.request.urlopen(api_url, timeout=5)
            data = json.loads(response.read().decode("utf-8"))
            return data.get("body", "No release notes available")
        except Exception as e:
            logger.warning(f"Failed to fetch release notes: {e}")
            return None


    def get_release_notes(self, release_url):
        """
        Extract release notes from release URL.

        Returns:
            str: Release notes or None if unavailable
        """
        try:
            # Convert GitHub web URL to API URL
            api_url = release_url.replace("releases/tag/", "releases/tags/")
            response = urllib.request.urlopen(api_url, timeout=5)
            data = json.loads(response.read().decode("utf-8"))
            return data.get("body", "No release notes available")
        except Exception as e:
            logger.warning(f"Failed to fetch release notes: {e}")
            return None
