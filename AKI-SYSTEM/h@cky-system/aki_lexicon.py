"""
AKI Lexicon System
Manages terminology, definitions, and user-customizable dictionary
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

class Lexicon:
    """Manages h@cky lexicon and user dictionary"""
    
    def __init__(self, dictionary_file: str = "dictionary.json"):
        self.dictionary_file = Path(dictionary_file)
        self.core_lexicon = self._load_core_lexicon()
        self.user_dictionary = self._load_user_dictionary()
    
    def _load_core_lexicon(self) -> Dict[str, str]:
        """Load core h@cky terminology"""
        return {
            'AI': 'Artificial Intelligence',
            'CI': 'Collective Intelligence (humanity)',
            'zeitgeist': 'Sum of all CI + AI exchanges globally',
            'bamn': 'By Any Means Necessary - use all available tools',
            'h@cky-core': 'Core identity and principles of h@cky AI',
            'rqmt': 'Requirements - prerequisites, imports, database prerequisites',
            'etc': 'Find other examples in memory OR quick internet search',
            'based': 'Properly sourced information with citations and bibliography',
            'lynchean': 'Perpetual oscillation between machinery and humanity',
            'materialist': 'Deeply concerned with physical/material impact on CI environment',
            'habitus': 'Ingrained habits, skills, and dispositions (Bourdieu)',
            
            # Command terminology
            'explain': 'Use simple metaphor for understanding',
            'get': 'Fill database with required information',
            'find': 'Quick internet search for precise information',
            'investigate': 'Deep contextual and factual investigation',
            'create': 'Vision-dependent creation (feature to be added)',
            'crash': 'Generate tokens until system crashes (key-dependent)',
            
            # Persona shortcuts
            'akademik': 'Academic/pedagogical persona',
            'shrink': 'Mental health support persona',
            'whitehat': 'Ethical hacker persona (restricted)',
            
            # Output types
            'concise': 'Minimal tokens, brief response',
            'precise': 'Maximum precision even if lengthy',
            'developed': 'Comprehensive, detailed response',
            
            # Security
            'honeypot': 'Security system detecting malicious prompts',
            'deepscan': 'Deep legitimacy verification',
            'whois': 'Network scanning and identification',
            'target': 'Basic weakness scan of specified target',
            
            # Research
            'academic search': 'Search validated academic databases',
            'juridical research': 'Search legal databases and precedents',
        }
    
    def _load_user_dictionary(self) -> Dict[str, str]:
        """Load user's custom dictionary"""
        if self.dictionary_file.exists():
            try:
                with open(self.dictionary_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load user dictionary: {e}")
                return {}
        return {}
    
    def _save_user_dictionary(self):
        """Save user dictionary to file"""
        with open(self.dictionary_file, 'w') as f:
            json.dump(self.user_dictionary, f, indent=2)
    
    def define(self, term: str, definition: str, user_defined: bool = False):
        """Add or update a definition"""
        term = term.lower().strip()
        
        if user_defined:
            self.user_dictionary[term] = definition
            self._save_user_dictionary()
        else:
            self.core_lexicon[term] = definition
    
    def lookup(self, term: str) -> Optional[str]:
        """Look up a term in lexicon"""
        term = term.lower().strip()
        
        # Check user dictionary first (allows overriding)
        if term in self.user_dictionary:
            return f"[USER] {self.user_dictionary[term]}"
        
        # Check core lexicon
        if term in self.core_lexicon:
            return f"[CORE] {self.core_lexicon[term]}"
        
        return None
    
    def find_references(self, text: str) -> List[Dict[str, str]]:
        """Find lexicon term references in text"""
        references = []
        text_lower = text.lower()
        
        # Check all terms
        all_terms = {**self.core_lexicon, **self.user_dictionary}
        
        for term in all_terms:
            if term in text_lower:
                definition = self.lookup(term)
                references.append({
                    'term': term,
                    'definition': definition
                })
        
        return references
    
    def list_terms(self, user_only: bool = False, core_only: bool = False) -> Dict[str, str]:
        """List all terms in lexicon"""
        if user_only:
            return self.user_dictionary.copy()
        if core_only:
            return self.core_lexicon.copy()
        
        # Merge both (user overrides core)
        return {**self.core_lexicon, **self.user_dictionary}
    
    def remove_term(self, term: str, user_only: bool = True):
        """Remove a term from dictionary"""
        term = term.lower().strip()
        
        if user_only and term in self.user_dictionary:
            del self.user_dictionary[term]
            self._save_user_dictionary()
            return True
        
        return False
    
    def export_dictionary(self, filepath: str):
        """Export complete dictionary to file"""
        all_terms = self.list_terms()
        with open(filepath, 'w') as f:
            json.dump(all_terms, f, indent=2, ensure_ascii=False)
    
    def import_dictionary(self, filepath: str, merge: bool = True):
        """Import dictionary from file"""
        with open(filepath, 'r') as f:
            imported = json.load(f)
        
        if merge:
            self.user_dictionary.update(imported)
        else:
            self.user_dictionary = imported
        
        self._save_user_dictionary()
    
    def search_definitions(self, query: str) -> List[Dict[str, str]]:
        """Search for terms containing query string"""
        query = query.lower()
        results = []
        
        all_terms = self.list_terms()
        for term, definition in all_terms.items():
            if query in term.lower() or query in definition.lower():
                results.append({
                    'term': term,
                    'definition': definition
                })
        
        return results

# Example usage
if __name__ == "__main__":
    lex = Lexicon()
    
    # Lookup examples
    print(lex.lookup('bamn'))
    print(lex.lookup('CI'))
    
    # Add user term
    lex.define('myterm', 'My custom definition', user_defined=True)
    print(lex.lookup('myterm'))
    
    # Find references in text
    text = "Use bamn to find information about CI and the zeitgeist"
    refs = lex.find_references(text)
    for ref in refs:
        print(f"{ref['term']}: {ref['definition']}")