"""
AKI Sandbox System
Safe Python execution environment
"""

import sys
import io
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import contextlib

class SandboxExecutor:
    """Execute Python code in sandboxed environment"""
    
    def __init__(self, sandbox_dir: str = "h@cky_system"):
        self.sandbox_dir = Path(sandbox_dir)
        self.sandbox_dir.mkdir(exist_ok=True)
        
        # Restricted imports for safety
        self.allowed_modules = {
            'math', 'random', 'datetime', 'json', 'csv',
            'collections', 're', 'itertools', 'functools',
            'pathlib', 'os.path', 'statistics'
        }
        
        # Dangerous functions to block
        self.blocked_builtins = {
            'eval', 'exec', 'compile', '__import__',
            'open', 'input', 'breakpoint'
        }
    
    def execute_python(self, code: str, timeout: int = 5) -> Dict[str, Any]:
        """
        Execute Python code with safety restrictions
        Returns dict with stdout, stderr, return_value, and success status
        """
        # Check for dangerous patterns
        safety_check = self._safety_check(code)
        if not safety_check['safe']:
            return {
                'success': False,
                'error': f"Safety violation: {safety_check['reason']}",
                'stdout': '',
                'stderr': safety_check['reason']
            }
        
        # Create restricted globals
        restricted_globals = self._create_restricted_globals()
        
        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = {
            'success': False,
            'stdout': '',
            'stderr': '',
            'return_value': None
        }
        
        try:
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):
                
                # Execute code
                exec_result = exec(code, restricted_globals)
                result['return_value'] = exec_result
                result['success'] = True
                
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {str(e)}"
            result['stderr'] = str(e)
        
        finally:
            result['stdout'] = stdout_capture.getvalue()
            if not result.get('stderr'):
                result['stderr'] = stderr_capture.getvalue()
        
        return result
    
    def execute_script(self, script_path: str, timeout: int = 10) -> Dict[str, Any]:
        """Execute a Python script file"""
        script_file = self.sandbox_dir / script_path
        
        if not script_file.exists():
            return {
                'success': False,
                'error': f"Script not found: {script_path}",
                'stdout': '',
                'stderr': f"File not found: {script_file}"
            }
        
        # Read and execute script
        with open(script_file, 'r') as f:
            code = f.read()
        
        return self.execute_python(code, timeout)
    
    def execute_shell(self, command: str, timeout: int = 10) -> Dict[str, Any]:
        """
        Execute shell command (with restrictions)
        DANGEROUS - Use with caution
        """
        # Block dangerous commands
        dangerous_commands = ['rm', 'sudo', 'chmod', 'dd', 'mkfs', ':(){']
        
        for dangerous in dangerous_commands:
            if dangerous in command.lower():
                return {
                    'success': False,
                    'error': f"Blocked dangerous command: {dangerous}",
                    'stdout': '',
                    'stderr': 'Command blocked for safety'
                }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.sandbox_dir
            )
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timeout',
                'stdout': '',
                'stderr': f'Command exceeded {timeout}s timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e)
            }
    
    def _safety_check(self, code: str) -> Dict[str, Any]:
        """Check code for dangerous patterns"""
        code_lower = code.lower()
        
        # Check for blocked builtins
        for blocked in self.blocked_builtins:
            if blocked in code_lower:
                return {
                    'safe': False,
                    'reason': f"Blocked builtin: {blocked}"
                }
        
        # Check for dangerous imports
        dangerous_imports = ['os', 'subprocess', 'sys', 'socket', 'requests']
        for dangerous in dangerous_imports:
            if f"import {dangerous}" in code_lower:
                return {
                    'safe': False,
                    'reason': f"Blocked import: {dangerous}"
                }
        
        # Check for file operations
        if 'open(' in code_lower or 'file(' in code_lower:
            return {
                'safe': False,
                'reason': "File operations not allowed in sandbox"
            }
        
        return {'safe': True}
    
    def _create_restricted_globals(self) -> Dict:
        """Create restricted global namespace"""
        # Start with safe builtins
        safe_builtins = {
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytes',
            'chr', 'dict', 'dir', 'divmod', 'enumerate', 'filter',
            'float', 'format', 'frozenset', 'hash', 'hex', 'int',
            'isinstance', 'issubclass', 'iter', 'len', 'list', 'map',
            'max', 'min', 'next', 'object', 'oct', 'ord', 'pow',
            'print', 'range', 'repr', 'reversed', 'round', 'set',
            'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip'
        }
        
        restricted = {
            '__builtins__': {name: getattr(__builtins__, name) 
                           for name in safe_builtins if hasattr(__builtins__, name)}
        }
        
        # Add allowed modules
        for module in self.allowed_modules:
            try:
                restricted[module] = __import__(module)
            except ImportError:
                pass
        
        return restricted
    
    def create_file(self, filename: str, content: str) -> bool:
        """Create a file in the sandbox"""
        filepath = self.sandbox_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def read_file(self, filename: str) -> Optional[str]:
        """Read a file from the sandbox"""
        filepath = self.sandbox_dir / filename
        
        if not filepath.exists():
            return None
        
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def list_files(self) -> list:
        """List files in sandbox"""
        return [f.name for f in self.sandbox_dir.iterdir() if f.is_file()]
    
    def cleanup(self):
        """Clean up sandbox directory"""
        import shutil
        if self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)
            self.sandbox_dir.mkdir()

# Example usage
if __name__ == "__main__":
    sandbox = SandboxExecutor()
    
    # Test safe code
    result = sandbox.execute_python("print('Hello from sandbox')")
    print("Safe code:", result)
    
    # Test blocked code
    result = sandbox.execute_python("import os; os.system('ls')")
    print("Blocked code:", result)