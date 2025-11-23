import sys
import time
import os
from pathlib import Path
from agents import Agent, Runner, function_tool
import asyncio

class Elect(Agent):

    
    def __init__(self):
        try:
            assert_ci_structure()
        except AssertionError:
            raise Exception(f"This Agent has no democratic structure - it will not run.")
        try:
            instructions = open(f"instructions.txt").read()
        except FileNotFoundError:
            raise FileNotFoundError(f"No instructions found!")
        super().__init__(f"Elect-{str(datetime.datetime.now())[:-7]}", instructions)
        
        
    def decide(self, case_id):
        response = asyncio.run(self, case_id)
        decision = response.final_output
        return decision

def decide(case_id):
    e = Elect()
    e.decide(case_id)

def assert_ci_structure():
    """
    Assert the presence of:
    
    .github/
        workflows/
            main.yml
            .voters.yml
            .voting.yml
            voting.yml
    relative to the current working directory.
    """
    root = Path.cwd()

    github = root / ".github"
    workflows = github / "workflows"

    required_files = [
        workflows / "main.yml",
        workflows / ".voters.yml",
        workflows / ".voting.yml",
        workflows / "voting.yml",
    ]

    # Directory checks
    if not github.is_dir():
        raise AssertionError(f"Missing directory: {github}")
    if not workflows.is_dir():
        raise AssertionError(f"Missing directory: {workflows}")

    # File checks
    for f in required_files:
        if not f.is_file():
            raise AssertionError(f"Missing file: {f}")

    return True
    
if __name__ == "__main__":
    e = Elect()
    e.decide()

