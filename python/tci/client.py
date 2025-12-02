import uuid
from dataclasses import dataclass, field
from typing import List, Any, Optional

@dataclass
class TestResult:
    name: str
    passed: bool
    reward: float

@dataclass
class Execution:
    stdout: str
    result: Any
    tests: List[TestResult] = field(default_factory=list)

@dataclass
class File:
    name: str
    content: bytes

class Session:
    def __init__(self, session_id, language="python"):
        self.id = session_id
        self.language = language

class TCIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tci.com"  # This will be the actual API endpoint
        self._session_files = {} # Mock file storage

    def _create_session(self, language="python"):
        session_id = str(uuid.uuid4())
        self._session_files[session_id] = {}
        return Session(session_id, language)

    def _close_session(self, session_id):
        # In a real implementation, this would make an API call to the backend
        # to terminate the session and clean up resources.
        if session_id in self._session_files:
            del self._session_files[session_id]
        print(f"Session {session_id} closed.")
        return True

    def _run_execution(self, session_id, code, tests):
        # Mock implementation: in a real scenario, this would call the TCI backend.
        print(f"Executing code in session {session_id}...")
        # Simulate execution
        stdout_mock = "The sum is 4"
        result_mock = 4

        # Simulate test evaluation
        test_results_mock = []
        if tests:
            for test in tests:
                # This is a mock evaluation. A real backend would evaluate `test["condition"]`.
                is_passed = "result == 4" in test.get("condition", "")
                test_results_mock.append(
                    TestResult(name=test["name"], passed=is_passed, reward=test["reward"] if is_passed else 0.0)
                )

        return Execution(stdout=stdout_mock, result=result_mock, tests=test_results_mock)

    def _upload_file(self, session_id, remote_path, content):
        if session_id not in self._session_files:
            raise ValueError("Session not found.")
        print(f"Uploading file {remote_path} to session {session_id}...")
        self._session_files[session_id][remote_path] = content
        return True

    def _download_file(self, session_id, remote_path):
        if session_id not in self._session_files or remote_path not in self._session_files[session_id]:
            raise FileNotFoundError(f"File '{remote_path}' not found in session '{session_id}'.")
        print(f"Downloading file {remote_path} from session {session_id}...")
        return File(name=remote_path, content=self._session_files[session_id][remote_path])


    @property
    def sessions(self):
        # Using a property to emulate the SDK design `tci.sessions.create()`
        return self.Sessions(self)

    @property
    def executions(self):
        return self.Executions(self)

    @property
    def files(self):
        return self.Files(self)

    class Sessions:
        def __init__(self, client):
            self._client = client

        def create(self, language="python"):
            return self._client._create_session(language)

        def close(self, session_id):
            return self._client._close_session(session_id)

    class Executions:
        def __init__(self, client):
            self._client = client

        def run(self, session_id: str, code: str, tests: Optional[List[dict]] = None):
            return self._client._run_execution(session_id, code, tests)

    class Files:
        def __init__(self, client):
            self._client = client

        def upload(self, session_id: str, remote_path: str, content: bytes):
            return self._client._upload_file(session_id, remote_path, content)

        def download(self, session_id: str, remote_path: str):
            return self._client._download_file(session_id, remote_path)
