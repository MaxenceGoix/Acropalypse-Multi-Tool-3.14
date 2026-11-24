import unittest
from pathlib import Path
from acropalypse import Acropalypse


class DetectorSmokeTests(unittest.TestCase):
    def test_demo_png_files_are_readable_by_detector(self):
        root = Path(__file__).resolve().parents[1] / "demo-images"
        detector = Acropalypse()
        for path in root.glob("*.png"):
            result = detector.detect_png(str(path))
            self.assertIsInstance(result, bool, path.name)


if __name__ == "__main__":
    unittest.main()
