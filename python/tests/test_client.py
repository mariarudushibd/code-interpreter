import unittest
from tci.client import TCIClient

class TestTCIClient(unittest.TestCase):

    def setUp(self):
        self.client = TCIClient(api_key="test_api_key")
        self.session = self.client.sessions.create()

    def tearDown(self):
        self.client.sessions.close(self.session.id)

    def test_session_creation_and_closing(self):
        # Session is created in setUp, so we just check it exists
        self.assertIsNotNone(self.session)
        self.assertIsNotNone(self.session.id)
        # Closing is tested in tearDown, but we can explicitly test it here too
        self.assertTrue(self.client.sessions.close(self.session.id))

    def test_code_execution(self):
        code = "result = 1 + 1"
        execution = self.client.executions.run(self.session.id, code)
        self.assertEqual(execution.result, 4)  # Mocked to return 4
        self.assertEqual(execution.stdout, "The sum is 4") # Mocked to return "The sum is 4"

    def test_code_execution_with_tests(self):
        code = "result = 4"
        tests = [{
            "name": "Check result",
            "condition": "result == 4",
            "reward": 1.0
        }]
        execution = self.client.executions.run(self.session.id, code, tests)
        self.assertTrue(execution.tests[0].passed)
        self.assertEqual(execution.tests[0].reward, 1.0)

    def test_file_upload_and_download(self):
        remote_path = "test.txt"
        file_content = b"Hello, TCI!"

        # Upload
        upload_success = self.client.files.upload(
            session_id=self.session.id,
            remote_path=remote_path,
            content=file_content
        )
        self.assertTrue(upload_success)

        # Download
        downloaded_file = self.client.files.download(
            session_id=self.session.id,
            remote_path=remote_path
        )
        self.assertEqual(downloaded_file.name, remote_path)
        self.assertEqual(downloaded_file.content, file_content)

    def test_download_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            self.client.files.download(self.session.id, "nonexistent.txt")

if __name__ == '__main__':
    unittest.main()
