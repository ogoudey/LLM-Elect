import sys
import time
import os
from pathlib import Path
from agents import Agent, Runner, function_tool
import asyncio
import datetime
import shutil



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
        
        
    def decide(self, prompt):
        print(f"{self.name} deciding...", end="\r")
        response = asyncio.run(Runner.run(self, prompt))
        decision = response.final_output
        print(f"{self.name} has decided.")
        return decision

def as_prompt(case: str) -> str:
    return f"Here is the case:\n{case}"

def decide(case_id):
    case = read_open_case(case_id)
    prompt = as_prompt(case)
    
    e = Elect()
    decision = e.decide(prompt)
    
    close_case(case_id, decision, e.name, e.instructions, prompt)


def list_open_cases():
    """
    Returns a list of case names (without .txt) from cases/open_cases/.
    """
    open_dir = Path("cases/open_cases")
    
    try:
        if not open_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {open_dir}")
    except FileNotFoundError:
        return []
    
    return [
        p.stem
        for p in open_dir.glob("*.txt")
        if p.is_file()
    ]
def write_open_case(case_id: str, content: str, overwrite: bool = False) -> Path:
    """
    Writes content to: cases/open_cases/<case_id>.txt
    Creates the directory if needed.
    
    If overwrite=False (default), raises an error if the case already exists.
    """
    path = Path("cases/open_cases") / f"{case_id}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not overwrite:
        raise FileExistsError(f"Open case already exists: {path}")

    path.write_text(content)
    return path
    
def read_open_case(case_id: str) -> str:
    """
    Reads: cases/open_cases/<case_id>.txt
    Returns its contents as a string.
    """
    path = Path("cases/open_cases") / f"{case_id}.txt"
    try:
        if not path.is_file():
            print(f"\nOpen case not found: {path}\n")
            raise FileNotFoundError(f"Open case not found: {path}")
    except FileNotFoundError:
        try:
            case = input("Write the case (^C to exit):\n\n>>> ")
            write_open_case(case_id, case, True)
            return read_open_case(case_id)
        except KeyboardInterrupt:
            raise FileNotFoundError(f"Won't make up new case...")
        
    return path.read_text()



def close_case(case_id: str, outcome: str, llm_name: str, llm_instructions: str, prompt: str):
    """
    Creates:
        cases/closed_cases/<case_id>/
            <case_id>.txt      # copy of open case
            outcome.txt          # written from 'outcome'
            <llm_name>.txt       # dump of llm_instructions
            prompt.txt           # dump of the prompt
    """
    base_open = Path("cases/open_cases") / f"{case_id}.txt"
    if not base_open.is_file():
        raise FileNotFoundError(f"Open case not found: {base_open}")

    

    closed_dir = Path("cases/closed_cases") / case_id
    
    if closed_dir.exists():
        input("Case with this ID already has already been closed.\n\tA. To overwrite press [enter].\n\tB. To exit do ^C.\n")
        shutil.rmtree(closed_dir)
            
    
    closed_dir.mkdir(parents=True, exist_ok=True)

    # A. Copy open case → <case_id>.txt
    shutil.copy(base_open, closed_dir / f"{case_id}.txt")

    # B. outcome.txt
    (closed_dir / "outcome.txt").write_text(outcome)

    # C. <llm_name>.txt (instructions dump)
    (closed_dir / f"{llm_name}.txt").write_text(llm_instructions)

    # D. prompt.txt
    (closed_dir / "prompt.txt").write_text(prompt)

    return closed_dir


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
    try:
        decide(sys.argv[1])
    except IndexError:
        open_cases_by_id = list_open_cases()
        if len(open_cases_by_id) > 0:
            print(f"Open cases:")
            for case_id in open_cases_by_id:
                print(case_id)
        decide(input("\nCase id: "))

