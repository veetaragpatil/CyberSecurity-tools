#!/usr/bin/env python3
import subprocess
import sys
import argparse
from typing import Dict, List

class Tool:
    def __init__(self, name: str, description: str, command: str):
        self.name = name
        self.description = description
        self.command = command

# Available tools registry
TOOLS: Dict[str, Tool] = {
    "subfinder": Tool(
        name="subfinder",
        description="Find subdomains using various sources",
        command="subfinder"
    ),
    "nmap": Tool(
        name="nmap", 
        description="Network scanning and discovery",
        command="nmap"
    ),
    "amass": Tool(
        name="amass",
        description="In-depth attack surface mapping and asset discovery", 
        command="amass"
    ),
    "whatweb": Tool(
        name="whatweb",
        description="Web technology identification",
        command="whatweb"
    )
}

def run_tool(tool: Tool, args: List[str]) -> tuple[str, int]:
    """Execute a tool with given arguments and return output and exit code"""
    try:
        cmd = [tool.command] + args
        print(f"Running: {' '.join(cmd)}")
        print("-" * 50)
        
        # Run the command and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False  # Don't raise exception on non-zero exit
        )
        
        return result.stdout + result.stderr, result.returncode
        
    except FileNotFoundError:
        return f"Error: Tool '{tool.command}' not found. Please install it first.", 1
    except Exception as e:
        return f"Error running {tool.name}: {str(e)}", 1

def print_usage():
    """Print usage information and available tools"""
    print("Security Tools CLI")
    print("=" * 30)
    print("\nUsage: python security-cli.py <tool> [options]")
    print("\nAvailable tools:")
    for name, tool in TOOLS.items():
        print(f"  {name:<12} - {tool.description}")
    print("\nExamples:")
    print("  python security-cli.py subfinder -d example.com")
    print("  python security-cli.py nmap -sV -p 80,443 example.com")
    print("  python security-cli.py amass enum -d example.com")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    tool_name = sys.argv[1]
    
    if tool_name not in TOOLS:
        print(f"Error: Tool '{tool_name}' not found")
        print_usage()
        sys.exit(1)
    
    # Get the tool and any additional arguments
    tool = TOOLS[tool_name]
    additional_args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Run the tool
    output, exit_code = run_tool(tool, additional_args)
    
    # Print output
    print(output)
    
    # Exit with the same code as the tool
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
