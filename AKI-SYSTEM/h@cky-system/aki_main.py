#!/usr/bin/env python3
"""
AKI System - Enhanced Terminal AI
Main entry point for the h@cky application
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from aki_core import AKICore
from aki_interface import AKIInterface
from aki_config import load_config, verify_prerequisites

def main():
    """Main entry point for AKI System"""
    
    # Display banner
    print("""
    ╔═══════════════════════════════════════╗
    ║     AKI SYSTEM - h@cky Terminal      ║
    ║    Enhanced AI Terminal Interface     ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Load configuration
    try:
        config = load_config()
        print("[✓] Configuration loaded")
    except Exception as e:
        print(f"[✗] Configuration error: {e}")
        sys.exit(1)
    
    # Verify prerequisites
    prereqs_status = verify_prerequisites()
    if not prereqs_status['all_ok']:
        print("\n[!] Missing prerequisites:")
        for prereq, status in prereqs_status['details'].items():
            symbol = "✓" if status else "✗"
            print(f"  [{symbol}] {prereq}")
        
        if input("\nContinue anyway? (y/n): ").lower() != 'y':
            sys.exit(1)
    else:
        print("[✓] All prerequisites verified")
    
    # Initialize core system
    try:
        aki_core = AKICore(config)
        print("[✓] AKI Core initialized")
    except Exception as e:
        print(f"[✗] Core initialization failed: {e}")
        sys.exit(1)
    
    # Launch interface
    try:
        interface = AKIInterface(aki_core, config)
        print("[✓] Interface ready\n")
        interface.run()
    except KeyboardInterrupt:
        print("\n\n[!] System interrupted by user")
    except Exception as e:
        print(f"\n[✗] Runtime error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n[✓] AKI System shutdown complete")

if __name__ == "__main__":
    main()