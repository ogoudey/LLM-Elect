### Why LLM agents can be helpful for organizations
- Time and cost saving.
- Objectivity - or at least, a non-individual's bias.

### What are the drawbacks
- There might not be agreement on the successfulness of the agent.
- The system prompts of the agents might not be transparent.

### Where LLM Elections might come in
Instead of having one agent designed, closed off, and evaluated by some external metric, the organization makes changes as a group to the instructions (system prompt) of the agent.
What if instead of a few individuals writing their own constitutions and then making decisions off of it, an organization instantiated an automated decision maker that followed a document chosen by the people.

### Use cases in mind
- Cooperative living arrangements
- Judicial systems, regulation
- A group of developers of agentic workflows
- Democratically run workplaces

### How to
#### Set up
1. clone repo
2. make fork
3. make initial instructions
4. configure `git-democracy`
#### Elections
1. make new branch
2. suggest edits
3. commit, push, and make pull request
4. vote on suggested edits (will pass or not)
#### Running
1. start up decision-maker ```python3 elected_llm.py```
2. select the open case
3. see folder structure for a history, making new cases, and seeing outcomes
