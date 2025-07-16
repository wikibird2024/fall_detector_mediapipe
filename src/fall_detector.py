import math


class FallDetector:
    def __init__(self, config):
        self.threshold = config["fall_threshold"]

    def is_fall(self, landmarks):
        try:
            shoulder = landmarks[11]
            hip = landmarks[23]
            angle = self._calculate_angle(shoulder, hip)
            return angle < self.threshold
        except:
            return False

    def _calculate_angle(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        angle = math.degrees(math.atan2(dy, dx))
        return abs(angle)
