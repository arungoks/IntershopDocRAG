"""
scraper/state.py
----------------
State checkpoint manager for tracking URL scraping status.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict, Dict


class UrlStateInfo(TypedDict):
    """Schema for individual URL state."""
    status: str
    retries: int
    last_attempt: str


class StateManager:
    """Manages processing state persistence to allow resuming scrapes."""

    def __init__(self, state_file: str | Path = "scrape_state.json") -> None:
        """Initialize the state manager.

        Parameters
        ----------
        state_file:
            Path to the JSON file tracking scrape state.
        """
        self.state_file: Path = Path(state_file)
        self.state: Dict[str, UrlStateInfo] = {}

        self._load()

    def _load(self) -> None:
        """Load state from file, or initialize empty if it doesn't exist."""
        if not self.state_file.exists():
            self.state = {}
            self._save()
        else:
            with self.state_file.open("r", encoding="utf-8") as f:
                try:
                    self.state = json.load(f)
                except json.JSONDecodeError:
                    # In a production system, we might want to backup the corrupted
                    # file instead of overwriting, but story AC defaults to
                    # recovering or ignoring if atomic guarantees failed (which
                    # they shouldn't with atomic saves).
                    self.state = {}
                    self._save()

    def _save(self) -> None:
        """Persist state to disk atomically to prevent corruption."""
        # Using atomic write: write to temp file on same filesystem, then atomic replace
        target_dir = self.state_file.parent
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # mkstemp provides secure file creation
        fd, temp_path = tempfile.mkstemp(
            dir=target_dir, prefix=f"{self.state_file.name}.tmp", text=True
        )
        
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
                
            # Atomically replace the existing state file
            os.replace(temp_path, self.state_file)
        except Exception:
            # Clean up the temporary file in case of crash/error before rename
            try:
                os.remove(temp_path)
            except OSError:
                pass
            raise

    def update_status(self, url: str, status: str, retries: int = 0) -> None:
        """Update the tracking status of a given URL.

        Parameters
        ----------
        url:
            The URL being processed.
        status:
            The result status (e.g., "success", "failed", "skipped").
        retries:
            The number of retry attempts made.
        """
        self.state[url] = {
            "status": status,
            "retries": retries,
            "last_attempt": datetime.now(timezone.utc).isoformat()
        }
        self._save()

    def should_skip(self, url: str) -> bool:
        """Check whether a URL has already been successfully processed.

        Parameters
        ----------
        url:
            The URL to check against the state.

        Returns
        -------
        bool
            True if the URL was previously processed with "success" status.
        """
        info = self.state.get(url)
        if not info:
            return False
            
        return info.get("status") == "success"
