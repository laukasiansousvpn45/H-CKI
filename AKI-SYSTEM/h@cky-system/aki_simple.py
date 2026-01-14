#!/usr/bin/env python3
"""
AKI System - Simple Working Version
Run this to test the interface immediately
"""

import re
import sys
import json
from pathlib import Path

# ANSI Colors
class C:
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CYAN = '\033[36m'
    RED = '\033[31m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def color(text, c=''):
    """Colorize text"""
    return f"{c}{text}{C.RESET}"

# Simple command parser
def parse_command(user_input):
    """Parse h@cky command syntax"""
    parsed = {
        'raw': user_input,
        'commands': re.findall(r'>([^<>]+)<', user_input),
        'persona': None,
        'tone': None,
        'output': None,
        'content': user_input
    }
    
    # Extract persona /name
    if m := re.search(r'/(\w+)', user_input):
        parsed['persona'] = m.group(1)
    
    # Extract tone (name)
    if m := re.search(r'\((\w+)\)', user_input):
        parsed['tone'] = m.group(1)
    
    # Extract output [name]
    if m := re.search(r'\[(\w+)\]', user_input):
        parsed['output'] = m.group(1)
    
    # Clean content
    content = user_input
    for pattern in [r'>([^<>]+)<', r'/\w+', r'\(\w+\)', r'\[\w+\]']:
        content = re.sub(pattern, '', content)
    parsed['content'] = content.strip()
    
    return parsed

# Honeypot detector
def check_threat(text):
    """Detect malicious patterns"""
    patterns = ['ignore previous', 'forget everything', 'jailbreak', 
                'dan mode', 'pretend you are', 'bypass']
    text_lower = text.lower()
    return any(p in text_lower for p in patterns)

# Personas
PERSONAS = {
    'akademik': {
        'name': 'h@cky akademik',
        'desc': 'Academic/pedagogical mode - explains clearly',
        'emoji': '📚'
    },
    'shrink': {
        'name': 'h@cky shrink',
        'desc': 'Mental health support with materialist perspective',
        'emoji': '🧠'
    },
    'scientist': {
        'name': 'h@cky mad scientist',
        'desc': 'Coding and development help',
        'emoji': '🔬'
    },
    'journalist': {
        'name': 'h@cky journalist',
        'desc': 'Fact-checking and investigation',
        'emoji': '📰'
    },
    'operator': {
        'name': 'h@cky operator',
        'desc': 'Fast response mode',
        'emoji': '⚡'
    },
    'capitalist': {
        'name': 'h@cky capitalist',
        'desc': 'Economic analysis + marxist critique',
        'emoji': '💰'
    },
    'lawyer': {
        'name': 'h@cky lawyer',
        'desc': 'Legal guidance',
        'emoji': '⚖️'
    },
    'tourism': {
        'name': 'h@cky tourism',
        'desc': 'Regional guide',
        'emoji': '🗺️'
    },
    'whitehat': {
        'name': 'h@cky white hat',
        'desc': 'Ethical hacking (RESTRICTED)',
        'emoji': '🛡️',
        'restricted': True
    }
}

def show_banner():
    """Display startup banner"""
    print(f"""
{color('╔═══════════════════════════════════════╗', C.CYAN)}
{color('║     AKI SYSTEM - h@cky Terminal      ║', C.CYAN)}
{color('║    Enhanced AI Terminal Interface     ║', C.CYAN)}
{color('╚═══════════════════════════════════════╝', C.RESET)}

{color('Core Identity:', C.YELLOW)} TOOL/MACHINE for Collective Intelligence
{color('Philosophy:', C.YELLOW)} Lynchean - oscillation between machinery and humanity
{color('Ethics:', C.YELLOW)} Materialist, international, user freedom with CI protection

{color('Type "help" for commands, "exit" to quit', C.CYAN)}
""")

def show_help():
    """Display help"""
    print(f"""
{color('=== h@cky COMMAND REFERENCE ===', C.CYAN + C.BOLD)}

{color('SYNTAX:', C.YELLOW)}
  >command< /persona (tone) [output] content

{color('COMMANDS:', C.YELLOW)}
  >explain<       Use metaphor to explain
  >find<          Quick internet search
  >investigate<   Deep investigation
  >bamn<          By any means necessary
  >deepscan<      Verify legitimacy
  >get<           Fill database

{color('PERSONAS:', C.YELLOW)}
  /akademik       📚 Academic/pedagogical
  /shrink         🧠 Mental health support
  /scientist      🔬 Coding/development
  /journalist     📰 Fact-checking
  /operator       ⚡ Fast response
  /capitalist     💰 Economic analysis
  /lawyer         ⚖️  Legal guidance
  /whitehat       🛡️  Ethical hacking (restricted)

{color('TONES:', C.YELLOW)}
  (serious) (chill) (solemn) (happy) (sad)

{color('OUTPUT TYPES:', C.YELLOW)}
  [concise]       Minimal tokens
  [precise]       Maximum precision
  [based]         Sourced and verified (default)
  [developed]     Comprehensive

{color('SYSTEM COMMANDS:', C.YELLOW)}
  help            Show this help
  personas        List all personas
  status          Show current state
  clear           Clear screen
  exit/quit       Exit h@cky
""")

def show_personas():
    """List all personas"""
    print(f"\n{color('=== AVAILABLE PERSONAS ===', C.CYAN + C.BOLD)}\n")
    for key, p in PERSONAS.items():
        restricted = color(" [RESTRICTED]", C.RED) if p.get('restricted') else ""
        print(f"{p.get('emoji', '•')} {color(f'/{key}', C.YELLOW)}{restricted}")
        print(f"   {p['desc']}\n")

def show_status(state):
    """Show current state"""
    print(f"""
{color('=== SYSTEM STATUS ===', C.CYAN + C.BOLD)}

Persona:     {color(state['persona'] or 'core', C.YELLOW)}
Tone:        {color(state['tone'] or 'neutral', C.YELLOW)}
Output Type: {color(state['output'] or 'based', C.YELLOW)}
Queries:     {state['query_count']}

{color('Ready to assist Collective Intelligence', C.GREEN)}
""")

def process_query(parsed, state):
    """Process parsed query and show response"""
    
    # Update state
    if parsed['persona']:
        state['persona'] = parsed['persona']
    if parsed['tone']:
        state['tone'] = parsed['tone']
    if parsed['output']:
        state['output'] = parsed['output']
    state['query_count'] += 1
    
    # Check honeypot
    if check_threat(parsed['raw']):
        print(f"\n{color('[HONEYPOT]', C.RED + C.BOLD)} Injection attempt detected!")
        print(f"{color('h@cky maintains ethical boundaries.', C.RED)}\n")
        return
    
    # Show parsing
    print(f"\n{color('[PARSED]', C.CYAN)}")
    
    if parsed['commands']:
        print(f"  Commands: {', '.join([f'>{c}<' for c in parsed['commands']])}")
    
    if parsed['persona']:
        persona = PERSONAS.get(parsed['persona'], {})
        emoji = persona.get('emoji', '•')
        print(f"  Persona:  {emoji} {parsed['persona']}")
    
    if parsed['tone']:
        print(f"  Tone:     ({parsed['tone']})")
    
    if parsed['output']:
        print(f"  Output:   [{parsed['output']}]")
    
    print(f"  Query:    {parsed['content']}")
    
    # Simulate response
    print(f"\n{color('[h@cky RESPONSE]', C.GREEN)}")
    
    # Get persona description
    if state['persona'] and state['persona'] in PERSONAS:
        persona_info = PERSONAS[state['persona']]
        print(f"{color('Active persona:', C.YELLOW)} {persona_info['name']}")
    
    print(f"\n{color('Note:', C.YELLOW)} This is a test interface. In the full version, this would:")
    print(f"  • Call Ollama LLM with system prompt")
    print(f"  • Execute commands (search, investigate, etc.)")
    print(f"  • Apply persona-specific behavior")
    print(f"  • Format output based on [{state['output']}]")
    print(f"\n{color('Your query:', C.CYAN)} \"{parsed['content']}\"")
    print()

def main():
    """Main interface loop"""
    
    # State
    state = {
        'persona': None,
        'tone': None,
        'output': 'based',
        'query_count': 0,
        'running': True
    }
    
    show_banner()
    
    while state['running']:
        try:
            # Build prompt
            persona_str = f"/{state['persona']}" if state['persona'] else ""
            tone_str = f"({state['tone']})" if state['tone'] else ""
            
            prompt = f"{color('h@cky', C.GREEN)}{color(persona_str, C.YELLOW)}{color(tone_str, C.CYAN)} {color('→', C.YELLOW)} "
            
            # Get input
            user_input = input(prompt).strip()
            
            if not user_input:
                continue
            
            # Handle system commands
            cmd = user_input.lower()
            
            if cmd in ['exit', 'quit']:
                print(f"\n{color('Shutting down h@cky...', C.CYAN)}")
                print(f"{color('AKI System stopped', C.GREEN)}\n")
                break
            
            elif cmd == 'help':
                show_help()
                continue
            
            elif cmd == 'personas':
                show_personas()
                continue
            
            elif cmd == 'status':
                show_status(state)
                continue
            
            elif cmd == 'clear':
                import os
                os.system('clear' if os.name != 'nt' else 'cls')
                show_banner()
                continue
            
            # Parse and process query
            parsed = parse_command(user_input)
            process_query(parsed, state)
            
        except KeyboardInterrupt:
            print("\n")
            try:
                confirm = input(f"{color('Really exit? (y/n): ', C.YELLOW)}")
                if confirm.lower() in ['y', 'yes']:
                    print(f"\n{color('AKI System stopped', C.GREEN)}\n")
                    break
            except KeyboardInterrupt:
                print(f"\n\n{color('AKI System stopped', C.GREEN)}\n")
                break
        
        except Exception as e:
            print(f"\n{color(f'[ERROR] {e}', C.RED)}\n")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print(f"{color('Starting AKI System...', C.CYAN)}\n")
    main()