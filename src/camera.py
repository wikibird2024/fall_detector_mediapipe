import cv2


class VideoStream:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)

    def __iter__(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
