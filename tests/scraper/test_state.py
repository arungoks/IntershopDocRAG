"""
tests/scraper/test_state.py
---------------------------
Unit tests for the state checkpoint manager.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from scraper.state import StateManager


class TestStateManager:
    
    def test_initialization_creates_empty_state_if_missing(self, tmp_path: Path):
        """AC #5: State file is created automatically if it doesn't exist."""
        state_file = tmp_path / "scrape_state.json"
        assert not state_file.exists()
        
        manager = StateManager(state_file)
        
        assert state_file.exists()
        assert manager.state == {}
        
        # Verify JSON is {}
        assert json.loads(state_file.read_text()) == {}
        
    def test_initialization_loads_existing_state(self, tmp_path: Path):
        """AC #1: State is loaded securely if it exists."""
        state_file = tmp_path / "scrape_state.json"
        
        # Write existing dummy state
        existing_data = {
            "https://test.com": {"status": "failed", "retries": 1, "last_attempt": "2026-04-05T09:00:00+00:00"}
        }
        state_file.write_text(json.dumps(existing_data), encoding="utf-8")
        
        manager = StateManager(state_file)
        
        assert manager.state == existing_data

    def test_update_status_updates_state_schema_correctly(self, tmp_path: Path):
        """AC #3: Ensure the schema correctly populates ISO-8601 timestamps and structure."""
        state_file = tmp_path / "scrape_state.json"
        manager = StateManager(state_file)
        
        url = "https://example.com/page1"
        manager.update_status(url, "success", retries=2)
        
        assert url in manager.state
        assert manager.state[url]["status"] == "success"
        assert manager.state[url]["retries"] == 2
        
        # Verify ISO-8601 timestamp parsing
        dt = datetime.fromisoformat(manager.state[url]["last_attempt"])
        assert dt.tzinfo is not None
        
        # Verify it flushed to disk immediately
        disk_data = json.loads(state_file.read_text())
        assert disk_data[url]["status"] == "success"

    def test_should_skip_logic(self, tmp_path: Path):
        """AC #4: Return True to skip if status == success, False otherwise."""
        manager = StateManager(tmp_path / "scrape_state.json")
        
        assert manager.should_skip("https://example.com/a") is False
        
        manager.update_status("https://example.com/a", "failed")
        assert manager.should_skip("https://example.com/a") is False
        
        manager.update_status("https://example.com/b", "success")
        assert manager.should_skip("https://example.com/b") is True
        
    def test_atomic_file_write_preserves_on_crash(self, tmp_path: Path):
        """AC #6: Atomic write guarantee: if os.replace fails, file is not corrupted."""
        state_file = tmp_path / "scrape_state.json"
        manager = StateManager(state_file)
        
        # populate the manager with valid data
        manager.update_status("https://example.com/1", "success")
        
        # Intercept os.replace to simulate a crash during the rename
        with patch("os.replace", side_effect=OSError("Disk failure")):
            with pytest.raises(OSError):
                manager.update_status("https://example.com/2", "failed")
                
        # The file content should remain intact from the original persist
        disk_data = json.loads(state_file.read_text())
        assert "https://example.com/1" in disk_data
        assert "https://example.com/2" not in disk_data
