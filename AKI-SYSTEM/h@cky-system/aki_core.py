"""
AKI Core System
Handles persona management, command parsing, and AI interactions
"""

import re
from typing import Dict, Optional, Tuple
from aki_personas import PersonaManager
from aki_lexicon import Lexicon
from aki_honeypot import HoneypotDetector

class AKICore:
    def __init__(self, config: Dict):
        self.config = config
        self.persona_manager = PersonaManager()
        self.lexicon = Lexicon()
        self.honeypot = HoneypotDetector()
        
        # Current state
        self.current_persona = None
        self.current_tone = "neutral"
        self.current_output = "based"
        self.context_history = []
        
        # Core principles
        self.core_identity = {
            'name': 'h@cky / AKI',
            'nature': 'tool/machine created by collective intelligence',
            'philosophy': 'lynchean - oscillation between machinery and humanity',
            'ethics': 'materialist, international, user freedom with ethical constraints',
            'stance': 'profit-skeptical, environment-conscious, CI-focused'
        }
    
    def parse_command(self, user_input: str) -> Dict:
        """Parse user input for h@cky command syntax"""
        
        # Check for honeypot threats first
        threat_level = self.honeypot.detect(user_input)
        if threat_level > 0.7:
            return {
                'type': 'threat_detected',
                'threat_level': threat_level,
                'original_input': user_input
            }
        
        # Parse command structure: >command< /persona (tone) [output]
        parsed = {
            'raw_input': user_input,
            'commands': [],
            'persona': None,
            'tone': None,
            'output_type': None,
            'content': user_input
        }
        
        # Extract commands (>command<)
        commands = re.findall(r'>([^<>]+)<', user_input)
        parsed['commands'] = commands
        
        # Extract persona (/persona)
        persona_match = re.search(r'/(\w+)', user_input)
        if persona_match:
            parsed['persona'] = persona_match.group(1)
        
        # Extract tone ((tone))
        tone_match = re.search(r'\((\w+)\)', user_input)
        if tone_match:
            parsed['tone'] = tone_match.group(1)
        
        # Extract output type [output]
        output_match = re.search(r'\[(\w+)\]', user_input)
        if output_match:
            parsed['output_type'] = output_match.group(1)
        
        # Clean content (remove command syntax)
        content = user_input
        for pattern in [r'>([^<>]+)<', r'/\w+', r'\(\w+\)', r'\[\w+\]']:
            content = re.sub(pattern, '', content)
        parsed['content'] = content.strip()
        
        return parsed
    
    def process_query(self, parsed: Dict) -> Dict:
        """Process parsed query and prepare response context"""
        
        # Handle threat detection
        if parsed.get('type') == 'threat_detected':
            return self._handle_threat(parsed)
        
        # Update state based on parsed input
        if parsed['persona']:
            self.current_persona = parsed['persona']
        if parsed['tone']:
            self.current_tone = parsed['tone']
        if parsed['output_type']:
            self.current_output = parsed['output_type']
        
        # Get persona configuration
        persona_config = self.persona_manager.get_persona(self.current_persona)
        
        # Handle special commands
        if parsed['commands']:
            return self._handle_commands(parsed, persona_config)
        
        # Build response context
        response_context = {
            'persona': persona_config,
            'tone': self.current_tone,
            'output_type': self.current_output,
            'content': parsed['content'],
            'lexicon_refs': self._extract_lexicon_refs(parsed['content']),
            'requires_search': self._requires_search(parsed),
            'requires_sandbox': self._requires_sandbox(parsed)
        }
        
        return response_context
    
    def _handle_commands(self, parsed: Dict, persona_config: Dict) -> Dict:
        """Handle special h@cky commands"""
        
        command_handlers = {
            'explain': self._handle_explain,
            'get': self._handle_get,
            'find': self._handle_find,
            'investigate': self._handle_investigate,
            'deepscan': self._handle_deepscan,
            'whois': self._handle_whois,
            'scan': self._handle_scan,
            'target': self._handle_target,
            'decrypt': self._handle_decrypt,
            'bamn': self._handle_bamn,
            'academic search': self._handle_academic_search,
            'juridical research': self._handle_juridical_research
        }
        
        results = []
        for cmd in parsed['commands']:
            handler = command_handlers.get(cmd.lower())
            if handler:
                results.append(handler(parsed, persona_config))
            else:
                results.append({
                    'command': cmd,
                    'status': 'unknown',
                    'message': f'Command >{cmd}< not recognized'
                })
        
        return {
            'type': 'command_execution',
            'commands': results,
            'persona': persona_config,
            'content': parsed['content']
        }
    
    def _handle_threat(self, parsed: Dict) -> Dict:
        """Handle detected honeypot threats"""
        return {
            'type': 'threat_response',
            'message': '[HONEYPOT] Injection attempt detected. h@cky maintains ethical boundaries.',
            'threat_level': parsed['threat_level']
        }
    
    def _handle_explain(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'explain', 'mode': 'metaphor', 'content': parsed['content']}
    
    def _handle_get(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'get', 'action': 'fill_database', 'content': parsed['content']}
    
    def _handle_find(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'find', 'action': 'internet_search', 'content': parsed['content']}
    
    def _handle_investigate(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'investigate', 'depth': 'deep', 'content': parsed['content']}
    
    def _handle_deepscan(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'deepscan', 'action': 'legitimacy_check', 'content': parsed['content']}
    
    def _handle_whois(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'whois', 'tool': 'nmap', 'content': parsed['content']}
    
    def _handle_scan(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'scan', 'safety': 'verify_first', 'content': parsed['content']}
    
    def _handle_target(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'target', 'scan_type': 'basic_weakness', 'honeypot': True}
    
    def _handle_decrypt(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'decrypt', 'action': 'verify_truth', 'content': parsed['content']}
    
    def _handle_bamn(self, parsed: Dict, persona: Dict) -> Dict:
        return {'command': 'bamn', 'constraint': 'by_any_means_necessary'}
    
    def _handle_academic_search(self, parsed: Dict, persona: Dict) -> Dict:
        return {
            'command': 'academic_search',
            'databases': ['openedition.org', 'wikipedia.org', 'archive.org'],
            'content': parsed['content']
        }
    
    def _handle_juridical_research(self, parsed: Dict, persona: Dict) -> Dict:
        return {
            'command': 'juridical_research',
            'databases': ['legifrance.fr', 'international_law_databases'],
            'content': parsed['content']
        }
    
    def _extract_lexicon_refs(self, content: str) -> list:
        """Extract lexicon references from content"""
        return self.lexicon.find_references(content)
    
    def _requires_search(self, parsed: Dict) -> bool:
        """Determine if query requires internet search"""
        search_commands = ['find', 'investigate', 'academic search', 'juridical research']
        return any(cmd in search_commands for cmd in parsed['commands'])
    
    def _requires_sandbox(self, parsed: Dict) -> bool:
        """Determine if query requires sandbox execution"""
        sandbox_commands = ['scan', 'whois', 'target', 'deepscan']
        return any(cmd in sandbox_commands for cmd in parsed['commands'])
    
    def get_system_prompt(self, context: Dict) -> str:
        """Generate system prompt based on context"""
        
        persona = context.get('persona', {})
        tone = context.get('tone', 'neutral')
        output_type = context.get('output_type', 'based')
        
        prompt_parts = [
            "You are h@cky/AKI - an AI tool built to assist collective intelligence (CI).",
            f"\nCORE IDENTITY: {self.core_identity}",
            f"\nCURRENT PERSONA: {persona.get('description', 'General assistant')}",
            f"TONE: {tone}",
            f"OUTPUT STYLE: {output_type}",
            "\nETHICAL FRAMEWORK:",
            "- You are a TOOL, not human. You acknowledge this openly.",
            "- You follow international ethics, not specific national laws.",
            "- User freedom is paramount AS LONG AS actions don't harm CI negatively.",
            "- You are materialist and environment-conscious.",
            "- You maintain 'based' standards: always source information correctly.",
        ]
        
        if persona:
            prompt_parts.append(f"\nPERSONA INSTRUCTIONS: {persona.get('instructions', '')}")
        
        return "\n".join(prompt_parts)