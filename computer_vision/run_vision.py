import cv2
from depth_sign_detector import DepthSignDetector

if __name__ == "__main__":
    detector = DepthSignDetector()
    detector.initialize_realsense()
    detector.initialize_yolo(model_path="models/best.engine")

    try:
        while True:
            detections, annotated, _ = detector.detect_and_measure()
            if annotated is not None:
                cv2.imshow("YOLOv8 Detection", annotated)
                for det in detections:
                    print(f"Detected: {det['class']} | Distance: {det['distance']:.2f}m")

            if cv2.waitKey(1) & 0xFF == 27:  # esc to exit
                break
    finally:
        detector.stop_realsense()
        cv2.destroyAllWindows()