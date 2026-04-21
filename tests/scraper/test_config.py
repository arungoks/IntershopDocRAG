"""
tests/scraper/test_config.py
----------------------------
Unit tests for configuration loading.
"""

from __future__ import annotations

import pytest
import yaml

from scraper.config import load_config

class TestConfigLoader:
    
    def test_load_valid_config(self, tmp_path):
        """Valid YAML config is correctly parsed into a dict."""
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text("sitemap_url: 'https://example.com/sitemap.xml'\nstart_url: 'https://example.com'", encoding="utf-8")
        
        config = load_config(cfg_path)
        
        assert config["sitemap_url"] == "https://example.com/sitemap.xml"
        assert config["start_url"] == "https://example.com"
        
    def test_missing_config_raises(self, tmp_path):
        """Missing config file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_config(tmp_path / "does_not_exist.yaml")
            
    def test_invalid_yaml_raises(self, tmp_path):
        """Invalid YAML syntax raises yaml.YAMLError."""
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text("sitemap_url: [unclosed list", encoding="utf-8")
        
        with pytest.raises(yaml.YAMLError):
            load_config(cfg_path)
