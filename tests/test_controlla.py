import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import ContainerEngine


class TestControlla(unittest.TestCase):
    @patch("shutil.which", return_value="/usr/local/bin/docker")
    @patch("subprocess.run")
    def test_list_containers(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='{"ID": "123456", "Image": "alpine", "Status": "Up 2 hours", "Names": "my_container"}\n',
            stderr="",
        )
        engine = ContainerEngine()
        containers = engine.list_containers()
        self.assertEqual(len(containers), 1)
        self.assertEqual(containers[0]["Names"], "my_container")

    @patch("shutil.which", return_value="/usr/local/bin/docker")
    @patch("subprocess.run")
    def test_start_and_stop_container(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(returncode=0, stdout="mock_container_id_hash\n", stderr="")
        engine = ContainerEngine()
        cid = engine.start_container(name="test_box", image="alpine:latest")
        self.assertEqual(cid, "mock_container_id_hash")

        ok = engine.stop_container("test_box")
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
