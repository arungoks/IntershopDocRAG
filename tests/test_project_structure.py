"""
Tests for Story 1.2: Scaffold Project Directory Structure & Configuration

Verifies all acceptance criteria:
AC1: Package directories exist with __init__.py files
AC2: data/raw_md/ and data/vectordb/ directories exist
AC3: config.yaml exists with all required keys
AC4: .gitignore excludes required files/directories
AC5: .streamlit/config.toml exists with Dark Mode theme values
AC6: tests/conftest.py exists
AC7: README.md exists with meaningful content
"""

from pathlib import Path
import yaml
import tomllib


PROJECT_ROOT = Path(__file__).parent.parent


class TestPackageDirectories:
    """AC1: Required package directories with __init__.py files."""

    REQUIRED_PACKAGES = [
        "scraper",
        "ingestion",
        "ui",
        "tests",
        "tests/scraper",
        "tests/ingestion",
        "tests/ui",
    ]

    def test_scraper_dir_exists(self):
        assert (PROJECT_ROOT / "scraper").is_dir()

    def test_ingestion_dir_exists(self):
        assert (PROJECT_ROOT / "ingestion").is_dir()

    def test_ui_dir_exists(self):
        assert (PROJECT_ROOT / "ui").is_dir()

    def test_tests_dir_exists(self):
        assert (PROJECT_ROOT / "tests").is_dir()

    def test_tests_scraper_dir_exists(self):
        assert (PROJECT_ROOT / "tests" / "scraper").is_dir()

    def test_tests_ingestion_dir_exists(self):
        assert (PROJECT_ROOT / "tests" / "ingestion").is_dir()

    def test_tests_ui_dir_exists(self):
        assert (PROJECT_ROOT / "tests" / "ui").is_dir()

    def test_scraper_init_exists(self):
        assert (PROJECT_ROOT / "scraper" / "__init__.py").exists()

    def test_ingestion_init_exists(self):
        assert (PROJECT_ROOT / "ingestion" / "__init__.py").exists()

    def test_ui_init_exists(self):
        assert (PROJECT_ROOT / "ui" / "__init__.py").exists()

    def test_tests_scraper_init_exists(self):
        assert (PROJECT_ROOT / "tests" / "scraper" / "__init__.py").exists()

    def test_tests_ingestion_init_exists(self):
        assert (PROJECT_ROOT / "tests" / "ingestion" / "__init__.py").exists()

    def test_tests_ui_init_exists(self):
        assert (PROJECT_ROOT / "tests" / "ui" / "__init__.py").exists()


class TestDataDirectories:
    """AC2: data/raw_md/ and data/vectordb/ must exist."""

    def test_data_raw_md_exists(self):
        assert (PROJECT_ROOT / "data" / "raw_md").is_dir()

    def test_data_vectordb_exists(self):
        assert (PROJECT_ROOT / "data" / "vectordb").is_dir()


class TestConfigYaml:
    """AC3: config.yaml with all required placeholder keys."""

    REQUIRED_KEYS = [
        "start_url",
        "sitemap_url",
        "ollama_port",
        "ollama_model",
        "embedding_model",
        "chroma_db_path",
        "raw_md_path",
        "chunk_size",
        "chunk_overlap",
    ]

    def test_config_yaml_exists(self):
        assert (PROJECT_ROOT / "config.yaml").exists()

    def test_config_yaml_parseable(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict), "config.yaml must be a valid YAML mapping"

    def test_config_yaml_has_start_url(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "start_url" in data

    def test_config_yaml_has_sitemap_url(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "sitemap_url" in data

    def test_config_yaml_has_ollama_port(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "ollama_port" in data

    def test_config_yaml_has_ollama_model(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "ollama_model" in data

    def test_config_yaml_has_embedding_model(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "embedding_model" in data

    def test_config_yaml_has_chroma_db_path(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "chroma_db_path" in data

    def test_config_yaml_has_raw_md_path(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "raw_md_path" in data

    def test_config_yaml_has_chunk_size(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "chunk_size" in data
        assert data["chunk_size"] == 2000

    def test_config_yaml_has_chunk_overlap(self):
        with open(PROJECT_ROOT / "config.yaml") as f:
            data = yaml.safe_load(f)
        assert "chunk_overlap" in data
        assert data["chunk_overlap"] == 200


class TestGitignore:
    """AC4: .gitignore excludes required sensitive/generated files."""

    def test_gitignore_exists(self):
        assert (PROJECT_ROOT / ".gitignore").exists()

    def _gitignore_lines(self):
        return (PROJECT_ROOT / ".gitignore").read_text()

    def test_gitignore_excludes_creds_txt(self):
        assert "creds.txt" in self._gitignore_lines()

    def test_gitignore_excludes_scrape_state(self):
        assert "scrape_state.json" in self._gitignore_lines()

    def test_gitignore_excludes_data_dir(self):
        assert "data/" in self._gitignore_lines()

    def test_gitignore_excludes_venv(self):
        content = self._gitignore_lines()
        assert ".venv" in content

    def test_gitignore_excludes_pycache(self):
        assert "__pycache__/" in self._gitignore_lines()


class TestStreamlitConfig:
    """AC5: .streamlit/config.toml with Dark Mode theme values."""

    def test_streamlit_config_toml_exists(self):
        assert (PROJECT_ROOT / ".streamlit" / "config.toml").exists()

    def test_streamlit_dark_background_color(self):
        with open(PROJECT_ROOT / ".streamlit" / "config.toml", "rb") as f:
            data = tomllib.load(f)
        assert data["theme"]["backgroundColor"] == "#0E1117"

    def test_streamlit_text_color(self):
        with open(PROJECT_ROOT / ".streamlit" / "config.toml", "rb") as f:
            data = tomllib.load(f)
        assert data["theme"]["textColor"] == "#FAFAFA"

    def test_streamlit_primary_color(self):
        with open(PROJECT_ROOT / ".streamlit" / "config.toml", "rb") as f:
            data = tomllib.load(f)
        assert data["theme"]["primaryColor"] == "#569CD6"


class TestConftest:
    """AC6: tests/conftest.py exists."""

    def test_conftest_exists(self):
        assert (PROJECT_ROOT / "tests" / "conftest.py").exists()


class TestReadme:
    """AC7: README.md exists with project overview and setup instructions."""

    def test_readme_exists(self):
        assert (PROJECT_ROOT / "README.md").exists()

    def test_readme_has_meaningful_content(self):
        content = (PROJECT_ROOT / "README.md").read_text()
        assert len(content) > 500, "README.md seems too short — should have real content"

    def test_readme_contains_setup_instructions(self):
        content = (PROJECT_ROOT / "README.md").read_text()
        assert "uv sync" in content, "README must mention 'uv sync' for setup"

    def test_readme_contains_usage(self):
        content = (PROJECT_ROOT / "README.md").read_text()
        assert "streamlit" in content.lower(), "README must mention Streamlit usage"
