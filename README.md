# code-interpreter

- Python & JS/TS SDK for running AI-generated code/code interpreting in your AI app? Bring Code Execution to Your AI Applications?  Execute LLM-generated code seamlessly with a simple API call. Code Interpreter (TCI) enables you to execute Python code in a sandboxed environment.
The Code Interpreter currently only supports Python. We plan to expand the language options in the future.

Reinforcement learning (RL) training: TCI transforms code execution into an interactive RL environment where generated code is run and evaluated in real time, providing reward signals from successes or failures, integrating automated pass/fail tests, and scaling easily across parallel workers—thus creating a powerful feedback loop that refines coding models over many trials.
Developing agentic workflows: TCI allows AI agents to seamlessly write and execute Python code, enabling robust, iterative, and secure computations within a closed-loop system.

## Python SDK Usage

### Installation

To install the TCI Python SDK, run the following command:

```bash
pip install tci
```

### Getting Started

Here's a simple example of how to use the TCI Python SDK to execute code:

```python
from tci import TCIClient

# 1. Initialize the client
tci = TCIClient(api_key="your_api_key")

# 2. Create a new session
session = tci.sessions.create(language="python")

try:
    # 3. Execute code
    code = "result = 1 + 1"
    execution = tci.executions.run(session.id, code)

    # 4. Process the results
    print(execution.stdout)
    print(execution.result)

finally:
    # 5. Clean up the session
    tci.sessions.close(session.id)
```

### File Management

You can also upload and download files to and from a session's ephemeral filesystem:

```python
# Upload a file
tci.files.upload(
    session_id=session.id,
    remote_path="data.csv",
    content=b"col1,col2\n1,2\n3,4"
)

# Download a file
downloaded_file = tci.files.download(
    session_id=session.id,
    remote_path="data.csv"
)

print(downloaded_file.name)
print(downloaded_file.content)
```

### API Overview

The `TCIClient` class is the main entry point for interacting with the TCI API. It provides the following methods:

- `tci.sessions.create()`: Creates a new session.
- `tci.sessions.close(session_id)`: Closes an existing session.
- `tci.executions.run(session_id, code, tests)`: Executes code in a session.
- `tci.files.upload(session_id, remote_path, content)`: Uploads a file to a session.
- `tci.files.download(session_id, remote_path)`: Downloads a file from a session.
