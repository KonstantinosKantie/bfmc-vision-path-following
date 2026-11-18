import cv2
import numpy as np
import pyrealsense2 as rs
from ultralytics import YOLO

class DepthSignDetector:
    def __init__(self):
        self.model = None
        self.pipeline = None
        self.align = None

    def initialize_realsense(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipeline.start(config)
        self.align = rs.align(rs.stream.color)

    def initialize_yolo(self, model_path="models/best.engine"):
        self.model = YOLO(model_path, task="detect")

    def stop_realsense(self):
        if self.pipeline:
            self.pipeline.stop()

    def detect_and_measure(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        if not color_frame or not depth_frame:
            return [], None, None

        frame = np.asanyarray(color_frame.get_data())
        depth = np.asanyarray(depth_frame.get_data())

        results = self.model(frame, verbose=False, conf=0.57)
        annotated = results[0].plot()
        detections = []

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            cls_id = int(box.cls[0])
            cls_name = self.model.names[cls_id]

            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
            cx = max(0, min(cx, 639))
            cy = max(0, min(cy, 479))
            distance = depth[cy, cx] / 1000.0

            dist_text = f"{distance:.2f}m" if distance > 0 else "N/A"
            cv2.putText(annotated, dist_text, (int(x1), int(y2) + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            detections.append({"class": cls_name, "distance": distance})

        return detections, annotated, frame