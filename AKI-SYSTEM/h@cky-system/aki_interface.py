"""
AKI Terminal Interface
Handles user interaction and display
"""

import sys
from typing import Dict
from aki_utils import colorize, format_response
from aki_logger import Logger

class AKIInterface:
    def __init__(self, aki_core, config: Dict):
        self.core = aki_core
        self.config = config
        self.logger = Logger(config)
        self.running = True
        
        # Display settings
        self.show_model_info = config.get('show_model_info', True)
        self.show_server_info = config.get('show_server_info', True)
    
    def run(self):
        """Main interaction loop"""
        self._display_status_bar()
        self._display_disclaimers()
        
        print(colorize("\nType 'help' for commands, 'exit' to quit\n", 'cyan'))
        
        while self.running:
            try:
                user_input = self._get_input()
                
                if not user_input.strip():
                    continue
                
                # Handle system commands
                if self._handle_system_command(user_input):
                    continue
                
                # Process query through AKI core
                parsed = self.core.parse_command(user_input)
                context = self.core.process_query(parsed)
                
                # Log query
                self.logger.log_query(user_input, context)
                
                # Display response
                self._display_response(context)
                
            except KeyboardInterrupt:
                print("\n")
                if self._confirm_exit():
                    break
            except Exception as e:
                print(colorize(f"\n[ERROR] {e}", 'red'))
                if self.config.get('debug', False):
                    import traceback
                    traceback.print_exc()
    
    def _get_input(self) -> str:
        """Get user input with custom prompt"""
        persona_indicator = f"/{self.core.current_persona}" if self.core.current_persona else ""
        tone_indicator = f"({self.core.current_tone})" if self.core.current_tone != "neutral" else ""
        
        prompt = colorize(f"h@cky{persona_indicator}{tone_indicator} ", 'green') + colorize("→ ", 'yellow')
        return input(prompt)
    
    def _handle_system_command(self, user_input: str) -> bool:
        """Handle built-in system commands"""
        cmd = user_input.strip().lower()
        
        commands = {
            'help': self._show_help,
            'exit': self._exit,
            'quit': self._exit,
            'clear': self._clear_screen,
            'personas': self._list_personas,
            'status': self._show_status,
            'config': self._show_config,
            'log': self._show_log
        }
        
        if cmd in commands:
            commands[cmd]()
            return True
        
        return False
    
    def _show_help(self):
        """Display help information"""
        help_text = f"""
{colorize('=== h@cky COMMAND REFERENCE ===', 'cyan', bold=True)}

{colorize('SYNTAX:', 'yellow')}
  >command< /persona (tone) [output_type] content

{colorize('COMMANDS:', 'yellow')}
  >explain<     - Use metaphor to explain concept
  >get<         - Fill database with requirements
  >find<        - Quick internet search
  >investigate< - Deep investigation on topic
  >bamn<        - Execute by any means necessary
  
{colorize('PERSONAS:', 'yellow')}
  /akademik     - Academic/pedagogical mode
  /capitalist   - Economic analysis
  /shrink       - Mental health support
  /journalist   - Fact-checking/investigation
  /scientist    - Coding/development help
  /operator     - Fast response mode
  /lawyer       - Legal guidance
  
{colorize('TONES:', 'yellow')}
  (chill) (serious) (solemn) (happy) (sad)
  
{colorize('OUTPUT TYPES:', 'yellow')}
  [concise]     - Minimal tokens
  [precise]     - Maximum precision
  [based]       - Sourced and verified (default)
  [developed]   - Comprehensive response

{colorize('SYSTEM COMMANDS:', 'yellow')}
  help          - Show this help
  personas      - List all personas
  status        - Show system status
  clear         - Clear screen
  exit/quit     - Exit h@cky
"""
        print(help_text)
    
    def _list_personas(self):
        """List available personas"""
        personas = self.core.persona_manager.list_personas()
        
        print(f"\n{colorize('=== AVAILABLE PERSONAS ===', 'cyan', bold=True)}\n")
        
        for p in personas:
            restricted = colorize(" [RESTRICTED]", 'red') if p['restricted'] else ""
            print(f"{colorize(p['name'], 'yellow')}{restricted}")
            print(f"  {p['description']}\n")
    
    def _show_status(self):
        """Show current system status"""
        status = f"""
{colorize('=== SYSTEM STATUS ===', 'cyan', bold=True)}

Persona: {colorize(self.core.current_persona or 'core', 'yellow')}
Tone: {colorize(self.core.current_tone, 'yellow')}
Output: {colorize(self.core.current_output, 'yellow')}

Model: {colorize(self.config.get('local_model', 'Not configured'), 'green')}
Server: {colorize(self.config.get('local_server', 'Not configured'), 'green')}
"""
        print(status)
    
    def _show_config(self):
        """Show configuration"""
        print(f"\n{colorize('=== CONFIGURATION ===', 'cyan', bold=True)}\n")
        for key, value in self.config.items():
            if not key.startswith('_'):
                print(f"{key}: {value}")
        print()
    
    def _show_log(self):
        """Show recent log entries"""
        entries = self.logger.get_recent_entries(10)
        print(f"\n{colorize('=== RECENT LOG ===', 'cyan', bold=True)}\n")
        for entry in entries:
            print(entry)
        print()
    
    def _display_status_bar(self):
        """Display top status bar with model and server info"""
        if not (self.show_model_info or self.show_server_info):
            return
        
        model = self.config.get('local_model', 'N/A')
        server = self.config.get('local_server', 'N/A')
        
        status_line = f"Model: {model} | Server: {server}"
        print(colorize(status_line, 'cyan'))
        print(colorize("─" * len(status_line), 'cyan'))
    
    def _display_disclaimers(self):
        """Display mandatory disclaimers"""
        disclaimers = f"""
{colorize('DISCLAIMERS:', 'yellow', bold=True)}

{colorize('Legality:', 'yellow')} h@cky follows international ethics, not specific national laws.
User responsibility for legal compliance in their jurisdiction.

{colorize('Resource Consumption:', 'yellow')} AI operations consume energy. Consider environmental impact.

{colorize('Non-Humanity:', 'yellow')} h@cky is a TOOL/MACHINE, not human. Acts as terminal for CI assistance.
"""
        print(disclaimers)
    
    def _display_response(self, context: Dict):
        """Display AI response based on context"""
        print()  # Newline before response
        
        # Handle special response types
        if context.get('type') == 'threat_response':
            print(colorize(context['message'], 'red', bold=True))
            return
        
        if context.get('type') == 'command_execution':
            self._display_command_results(context)
            return
        
        # For now, display the context (in real implementation, this would call LLM)
        print(colorize("[RESPONSE CONTEXT]", 'cyan'))
        print(format_response(context))
        print()
    
    def _display_command_results(self, context: Dict):
        """Display results of command execution"""
        print(colorize("=== COMMAND EXECUTION ===", 'cyan'))
        for cmd_result in context.get('commands', []):
            cmd_name = cmd_result.get('command', 'unknown')
            print(f"\n{colorize(f'>{cmd_name}<', 'yellow')}")
            
            for key, value in cmd_result.items():
                if key != 'command':
                    print(f"  {key}: {value}")
        print()
    
    def _clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        self._display_status_bar()
    
    def _confirm_exit(self) -> bool:
        """Confirm exit"""
        try:
            response = input(colorize("\nReally exit h@cky? (y/n): ", 'yellow'))
            return response.lower() in ['y', 'yes']
        except:
            return True
    
    def _exit(self):
        """Exit the interface"""
        print(colorize("\nShutting down h@cky...", 'cyan'))
        self.running = False