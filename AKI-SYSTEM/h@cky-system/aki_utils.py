"""
AKI Utility Functions
Helper functions for formatting, display, and common operations
"""

import json
from typing import Any, Dict

# ANSI color codes
COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

def colorize(text: str, color: str = 'white', bold: bool = False, underline: bool = False) -> str:
    """Add ANSI color codes to text"""
    codes = []
    
    if bold:
        codes.append(COLORS['bold'])
    if underline:
        codes.append(COLORS['underline'])
    if color in COLORS:
        codes.append(COLORS[color])
    
    if not codes:
        return text
    
    return ''.join(codes) + text + COLORS['reset']

def format_response(data: Any, indent: int = 2) -> str:
    """Format data for display"""
    if isinstance(data, dict):
        return json.dumps(data, indent=indent, ensure_ascii=False)
    return str(data)

def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove null bytes and excessive whitespace
    text = text.replace('\x00', '')
    text = ' '.join(text.split())
    return text.strip()

def parse_key_value(text: str, separator: str = '=') -> Dict[str, str]:
    """Parse key=value pairs from text"""
    result = {}
    for line in text.split('\n'):
        line = line.strip()
        if separator in line:
            key, value = line.split(separator, 1)
            result[key.strip()] = value.strip()
    return result

def format_table(headers: list, rows: list) -> str:
    """Format data as ASCII table"""
    if not rows:
        return "No data"
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))
    
    # Rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        lines.append(row_line)
    
    return "\n".join(lines)

def bytes_to_human(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def dict_to_args(d: Dict) -> str:
    """Convert dictionary to command-line argument string"""
    args = []
    for key, value in d.items():
        if isinstance(value, bool):
            if value:
                args.append(f"--{key}")
        else:
            args.append(f"--{key}={value}")
    return " ".join(args)

class ProgressBar:
    """Simple progress bar for terminal"""
    
    def __init__(self, total: int, width: int = 50, prefix: str = 'Progress'):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.current = 0
    
    def update(self, amount: int = 1):
        """Update progress bar"""
        self.current += amount
        self._draw()
    
    def _draw(self):
        """Draw progress bar"""
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        print(f'\r{self.prefix}: |{bar}| {percent*100:.1f}%', end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete

def confirm_action(message: str, default: bool = False) -> bool:
    """Ask user to confirm an action"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{message} ({default_str}): ").strip().lower()
    
    if not response:
        return default
    
    return response in ['y', 'yes']

def format_error(error: Exception, include_trace: bool = False) -> str:
    """Format error message"""
    msg = f"[ERROR] {type(error).__name__}: {str(error)}"
    
    if include_trace:
        import traceback
        msg += "\n" + traceback.format_exc()
    
    return colorize(msg, 'red')