"""
AKI Logging System
Manages encrypted conversation logs
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import deque

class Logger:
    """Manages encrypted conversation logs"""
    
    def __init__(self, config: Dict):
        self.log_file = Path(config.get('log_file', 'aki.log'))
        self.encrypted = config.get('log_encrypted', True)
        self.max_memory_entries = 100
        
        # In-memory recent entries
        self.recent_entries = deque(maxlen=self.max_memory_entries)
        
        # Ensure log file exists
        if not self.log_file.exists():
            self.log_file.touch()
    
    def log_query(self, query: str, context: Dict):
        """Log a user query and its context"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'query',
            'query': query,
            'persona': context.get('persona', {}).get('name', 'core'),
            'tone': context.get('tone', 'neutral'),
            'output_type': context.get('output_type', 'based'),
            'commands': context.get('commands', []),
        }
        
        self._write_entry(entry)
    
    def log_response(self, response: str, context: Dict):
        """Log an AI response"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'response',
            'response': response,
            'persona': context.get('persona', {}).get('name', 'core'),
        }
        
        self._write_entry(entry)
    
    def log_event(self, event_type: str, data: Dict):
        """Log a system event"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'event',
            'event_type': event_type,
            'data': data
        }
        
        self._write_entry(entry)
    
    def log_error(self, error: Exception, context: Optional[Dict] = None):
        """Log an error"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self._write_entry(entry)
    
    def _write_entry(self, entry: Dict):
        """Write entry to log file"""
        # Add to recent entries
        self.recent_entries.append(entry)
        
        # Prepare entry
        if self.encrypted:
            entry_str = self._encrypt_entry(entry)
        else:
            entry_str = json.dumps(entry)
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(entry_str + '\n')
    
    def _encrypt_entry(self, entry: Dict) -> str:
        """
        Simple encryption for log entries
        NOTE: This is basic obfuscation. For production, use proper encryption.
        """
        entry_str = json.dumps(entry)
        
        # Simple hash-based obfuscation
        # In production, use cryptography library with proper encryption
        entry_bytes = entry_str.encode('utf-8')
        
        # XOR with a derived key (NOT SECURE - for demonstration only)
        key = hashlib.sha256(b'aki_log_key').digest()
        encrypted = bytearray()
        
        for i, byte in enumerate(entry_bytes):
            encrypted.append(byte ^ key[i % len(key)])
        
        # Return as hex
        return encrypted.hex()
    
    def _decrypt_entry(self, encrypted_hex: str) -> Dict:
        """Decrypt a log entry"""
        try:
            encrypted = bytes.fromhex(encrypted_hex)
            key = hashlib.sha256(b'aki_log_key').digest()
            
            decrypted = bytearray()
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key[i % len(key)])
            
            entry_str = decrypted.decode('utf-8')
            return json.loads(entry_str)
        except:
            return None
    
    def get_recent_entries(self, count: int = 10) -> List[str]:
        """Get recent log entries (from memory)"""
        entries = list(self.recent_entries)[-count:]
        return [self._format_entry(e) for e in entries]
    
    def _format_entry(self, entry: Dict) -> str:
        """Format entry for display"""
        timestamp = entry.get('timestamp', 'N/A')
        entry_type = entry.get('type', 'unknown')
        
        if entry_type == 'query':
            return f"[{timestamp}] QUERY ({entry.get('persona')}): {entry.get('query', '')[:50]}..."
        elif entry_type == 'response':
            return f"[{timestamp}] RESPONSE: {entry.get('response', '')[:50]}..."
        elif entry_type == 'event':
            return f"[{timestamp}] EVENT: {entry.get('event_type')}"
        elif entry_type == 'error':
            return f"[{timestamp}] ERROR: {entry.get('error_type')} - {entry.get('error_message')}"
        
        return f"[{timestamp}] {entry_type.upper()}"
    
    def read_log(self, count: Optional[int] = None, decrypt: bool = None) -> List[Dict]:
        """Read entries from log file"""
        if decrypt is None:
            decrypt = self.encrypted
        
        entries = []
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        # Get last N lines if count specified
        if count:
            lines = lines[-count:]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if decrypt:
                entry = self._decrypt_entry(line)
            else:
                try:
                    entry = json.loads(line)
                except:
                    entry = None
            
            if entry:
                entries.append(entry)
        
        return entries
    
    def search_log(self, query: str, decrypt: bool = None) -> List[Dict]:
        """Search log for entries containing query"""
        entries = self.read_log(decrypt=decrypt)
        query_lower = query.lower()
        
        results = []
        for entry in entries:
            entry_str = json.dumps(entry).lower()
            if query_lower in entry_str:
                results.append(entry)
        
        return results
    
    def clear_log(self, confirm: bool = False):
        """Clear the log file"""
        if not confirm:
            raise ValueError("Must confirm log clearing with confirm=True")
        
        self.log_file.unlink()
        self.log_file.touch()
        self.recent_entries.clear()
    
    def export_log(self, output_file: str, decrypt: bool = True):
        """Export log to readable file"""
        entries = self.read_log(decrypt=decrypt)
        
        with open(output_file, 'w') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self) -> Dict:
        """Get log statistics"""
        entries = self.read_log()
        
        stats = {
            'total_entries': len(entries),
            'by_type': {},
            'by_persona': {},
            'date_range': {
                'first': entries[0]['timestamp'] if entries else None,
                'last': entries[-1]['timestamp'] if entries else None
            }
        }
        
        for entry in entries:
            # Count by type
            entry_type = entry.get('type', 'unknown')
            stats['by_type'][entry_type] = stats['by_type'].get(entry_type, 0) + 1
            
            # Count by persona (for queries and responses)
            if 'persona' in entry:
                persona = entry['persona']
                stats['by_persona'][persona] = stats['by_persona'].get(persona, 0) + 1
        
        return stats