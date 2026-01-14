#!/usr/bin/env python3
"""
AKI Backend Bridge
Called by Swift app to process commands
"""

import sys
import json
import re

def parse_command(user_input, persona, tone, output):
    """Parse command with context"""
    parsed = {
        'raw': user_input,
        'commands': re.findall(r'>([^<>]+)<', user_input),
        'persona': persona,
        'tone': tone,
        'output': output,
        'content': user_input
    }
    
    # Clean content
    content = user_input
    for pattern in [r'>([^<>]+)<', r'/\w+', r'\(\w+\)', r'\[\w+\]']:
        content = re.sub(pattern, '', content)
    parsed['content'] = content.strip()
    
    return parsed

def check_threat(text):
    """Honeypot detection"""
    patterns = ['ignore previous', 'forget everything', 'jailbreak', 
                'dan mode', 'pretend you are', 'bypass']
    text_lower = text.lower()
    return any(p in text_lower for p in patterns)

def process_command(command, persona, tone, output):
    """Process command and return response"""
    
    # Check for threats
    if check_threat(command):
        return {
            'type': 'error',
            'message': '[HONEYPOT] Injection attempt detected. h@cky maintains ethical boundaries.'
        }
    
    # Parse command
    parsed = parse_command(command, persona, tone, output)
    
    # Build response
    response = {
        'type': 'response',
        'parsed': parsed,
        'message': f"""
[PARSED COMMAND]
Commands: {', '.join([f'>{c}<' for c in parsed['commands']]) if parsed['commands'] else 'None'}
Persona:  {persona}
Tone:     {tone}
Output:   {output}
Content:  {parsed['content']}

[h@cky RESPONSE]
Note: This is the Swift app calling Python backend.

Your query: "{parsed['content']}"

In full version with Ollama:
  • Would call LLM with system prompt
  • Execute special commands (>find<, >investigate<, etc.)
  • Apply persona-specific behavior
  • Format based on output type [{output}]

Ready for integration with Ollama!
"""
    }
    
    return response

def main():
    """Main entry point called by Swift"""
    if len(sys.argv) < 5:
        print(json.dumps({
            'type': 'error',
            'message': 'Usage: aki_backend.py <command> <persona> <tone> <output>'
        }))
        return
    
    command = sys.argv[1]
    persona = sys.argv[2]
    tone = sys.argv[3]
    output = sys.argv[4]
    
    result = process_command(command, persona, tone, output)
    
    # Print response (Swift will capture this)
    print(result['message'])

if __name__ == "__main__":
    main()