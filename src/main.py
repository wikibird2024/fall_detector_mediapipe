import cv2

from src.alert import Alert
from src.camera import VideoStream
from src.config import load_config
from src.fall_detector import FallDetector
from src.pose_estimator import PoseEstimator


def main():
    config = load_config("configs/config.yaml")
    pose_estimator = PoseEstimator()
    fall_detector = FallDetector(config)
    alert = Alert(config)
    stream = VideoStream(index=config["camera_index"])

    for frame in stream:
        landmarks = pose_estimator.get_landmarks(frame)
        if landmarks:
            if fall_detector.is_fall(landmarks):
                alert.trigger("Fall detected!")
        cv2.imshow("Fall Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
