"""
AKI Configuration Management
Handles configuration loading and prerequisite verification
"""

import os
import json
from pathlib import Path
from typing import Dict

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "local_server": "ollama",
    "local_model": "deepseek",
    "remote_server": "",
    "database_file": "database.txt",
    "database_url": "www.database.exemple.net",
    "show_model_info": True,
    "show_server_info": True,
    "enable_sandbox": False,
    "enable_tor": False,
    "log_file": "aki.log",
    "log_encrypted": True,
    "debug": False,
    "honeypot_enabled": True,
    "academic_databases": [
        "openedition.org",
        "wikipedia.org",
        "archive.org"
    ],
    "juridical_databases": [
        "legifrance.fr"
    ]
}

def load_config() -> Dict:
    """Load configuration from file or create default"""
    config_path = Path(CONFIG_FILE)
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Merge with defaults for any missing keys
        return {**DEFAULT_CONFIG, **config}
    else:
        # Create default config file
        with open(config_path, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"[!] Created default config at {config_path}")
        return DEFAULT_CONFIG

def save_config(config: Dict):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def verify_prerequisites() -> Dict:
    """
    Verify system prerequisites
    Returns dict with 'all_ok' boolean and 'details' dict
    """
    prereqs = {
        'python': _check_python(),
        'ollama': _check_ollama(),
        'tor': _check_tor(),
        'nmap': _check_nmap(),
        'homebrew': _check_homebrew(),
        'pip': _check_pip(),
        'chromedriver': _check_chromedriver(),
        'selenium': _check_python_package('selenium'),
        'tavily': _check_python_package('tavily'),
    }
    
    all_ok = all(prereqs.values())
    
    return {
        'all_ok': all_ok,
        'details': prereqs
    }

def _check_python() -> bool:
    """Check if Python 3.7+ is available"""
    import sys
    return sys.version_info >= (3, 7)

def _check_command(cmd: str) -> bool:
    """Check if a command is available in PATH"""
    import shutil
    return shutil.which(cmd) is not None

def _check_ollama() -> bool:
    """Check if Ollama is installed"""
    return _check_command('ollama')

def _check_tor() -> bool:
    """Check if Tor is installed"""
    # Check for tor command or Tor Browser
    return _check_command('tor') or os.path.exists('/Applications/Tor Browser.app')

def _check_nmap() -> bool:
    """Check if nmap is installed"""
    return _check_command('nmap')

def _check_homebrew() -> bool:
    """Check if Homebrew is installed (macOS)"""
    return _check_command('brew')

def _check_pip() -> bool:
    """Check if pip is installed"""
    return _check_command('pip') or _check_command('pip3')

def _check_chromedriver() -> bool:
    """Check if chromedriver is installed"""
    return _check_command('chromedriver')

def _check_python_package(package: str) -> bool:
    """Check if a Python package is installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def get_prerequisites_install_guide() -> str:
    """Return installation guide for prerequisites"""
    return """
=== PREREQUISITES INSTALLATION GUIDE ===

1. Homebrew (macOS package manager):
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Ollama (local LLM server):
   brew install ollama
   ollama pull deepseek

3. Tor Browser:
   brew install --cask tor-browser
   
4. nmap (network scanner):
   brew install nmap

5. Python packages:
   pip install selenium tavily-python requests beautifulsoup4

6. ChromeDriver:
   brew install --cask chromedriver

7. Optional - ROBIN AI and other tools:
   # Configure in config.json as needed
"""