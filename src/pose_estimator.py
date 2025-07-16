import cv2
import mediapipe as mp


class PoseEstimator:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        self.drawing = mp.solutions.drawing_utils
        self.connections = mp.solutions.pose.POSE_CONNECTIONS

        # Check if drawing_styles has the newer pose styling methods
        try:
            from mediapipe.python.solutions import drawing_styles

            self.landmark_style = drawing_styles.get_default_pose_landmarks_style()
            self.connection_style = drawing_styles.get_default_pose_connections_style()
            self.use_default_styles = True
        except (ImportError, AttributeError):
            self.landmark_style = self.drawing.DrawingSpec(
                color=(0, 255, 0), thickness=2, circle_radius=2
            )
            self.connection_style = self.drawing.DrawingSpec(
                color=(255, 0, 0), thickness=2
            )
            self.use_default_styles = False

    def get_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(frame_rgb)

        if result.pose_landmarks:
            self.drawing.draw_landmarks(
                image=frame,
                landmark_list=result.pose_landmarks,
                connections=self.connections,
                landmark_drawing_spec=self.landmark_style,
                connection_drawing_spec=self.connection_style,
            )
            return result.pose_landmarks.landmark

        return None
