# Autonomous Driving Modules – BFMC (Bosch Future Mobility Challenge) 🚗

This repository showcases my core software, computer vision, and embedded systems contributions to our team's autonomous vehicle for the **Bosch Future Mobility Challenge (BFMC)**. My work focused on **real-time object & depth detection (YOLOv8 TensorRT + RealSense)**, **graph-based odometry path following (Stanley Controller)**, and **edge deployment on NVIDIA Jetson (Linux)**.

---

## 🎥 System Demos

### 1. Stop Sign Detection & Depth-Based Braking (YOLOv8 + RealSense)
*(Σύρε εδώ το `stop_sign_demo.mp4`)*

### 2. Crosswalk / Pedestrian Detection
*(Σύρε εδώ το `crosswalk_demo.mp4`)*

### 3. Odometry Path Following on Difficult Turns (Stanley Controller)
*(Σύρε εδώ το `turn_path_following.mp4`)*

---

## 🎯 Key Contributions

### 1. Computer Vision & Depth Estimation (YOLOv8 + TensorRT + RealSense)
* **Custom Dataset & Training:** Built and curated a custom dataset of **~5,000 track images** and trained a **YOLOv8** object detection model (~60 epochs) to recognize traffic signs, crosswalks, pedestrians, and obstacles.
* **TensorRT Optimization:** Exported the trained model to an **NVIDIA TensorRT engine (`best.engine`)** for low-latency, real-time GPU inference on the edge.
* **RGB-D Distance Estimation:** Integrated an **Intel RealSense** camera with pixel-to-pixel depth-to-color alignment (`pyrealsense2`) to calculate the exact real-world distance (in meters) to every detected object.

### 2. Graph-Based Odometry Path Following (Stanley Controller)
* **Engineering Motivation (Redundancy & Edge Cases):** Standard vision-based lane following struggles in tight intersections or track segments with missing outer lane markings. To solve this, we built an odometry-based path follower to act both as a specialized controller for difficult turns and as a **redundant backup navigation system**.
* **How It Works:** Using the vehicle's localized pose and heading vector (from IMU/odometry fusion), the module constructs a reference line segment between consecutive track graph nodes (`GraphML`) and computes the **heading error** and **crosstrack error** via geometric calculations (`SymPy`).
* **Control:** Feeds the errors into a **Stanley Controller** to output smooth, bounded steering commands.
* *Collaboration:* Developed in collaboration with **NLattas** (primary contributor to the graph coordinate utilities) and **Vaios Kakae**.

![BFMC Track Graph with Nodes](assets/TrackWithNodes.jpg)

### 3. Edge Deployment & Linux Administration (NVIDIA Jetson)
* Set up, configured, and maintained the **Linux (Ubuntu / JetPack)** environment on the **NVIDIA Jetson** onboard computer.
* Handled hardware interfacing, camera pipelines, and real-time execution of the perception and navigation modules.

---

## 🛠️ Tech Stack
* **Languages:** Python
* **Computer Vision & AI:** Ultralytics YOLOv8, NVIDIA TensorRT, OpenCV, Intel RealSense SDK (`pyrealsense2`)
* **Navigation & Control:** Stanley Controller, NetworkX (GraphML), SymPy, NumPy
* **Hardware & OS:** NVIDIA Jetson, Linux (Ubuntu / JetPack), Intel RealSense Depth Camera

---

## 📂 Repository Structure
```text
├── computer_vision/
│   ├── depth_sign_detector.py   # Modular YOLOv8 TensorRT + RealSense depth class
│   └── run_vision.py            # Live inference and visualization script
├── path_following/
│   ├── odometry_following.py    # Graph-based Stanley Controller implementation
│   └── xy_to_node.py            # GraphML parsing and node-coordinate mapping
└── assets/                      # Track node maps and demo media
