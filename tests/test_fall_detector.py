import unittest

from src.fall_detector import FallDetector


class DummyLandmark:
    def __init__(self, x, y):
        self.x, self.y = x, y


class TestFallDetector(unittest.TestCase):
    def test_fall_detection(self):
        fd = FallDetector({"fall_threshold": 45})
        landmarks = [None] * 33
        landmarks[11] = DummyLandmark(0.5, 0.2)  # shoulder
        landmarks[23] = DummyLandmark(0.5, 0.6)  # hip
        self.assertTrue(fd.is_fall(landmarks))


if __name__ == "__main__":
    unittest.main()
