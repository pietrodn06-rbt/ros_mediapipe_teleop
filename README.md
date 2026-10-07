# ROS MediaPipe Gesture Teleoperation System

A lightweight ROS 1 / Python package enabling real-time hand gesture tracking via OpenCV and Google MediaPipe to teleoperate mobile robots (e.g., TurtleBot3 / Gazebo simulations) using normalized kinematic mapping.

## Overview
This repository provides a computer vision pipeline that maps hand keypoint coordinates detected from a webcam feed into standard ROS linear and angular velocity commands (`geometry_msgs/Twist`).

## Features
- **Real-time Tracking:** Low-latency landmark detection using Google MediaPipe.
- **ROS Integration:** Publishes directly to the `/cmd_vel` topic at 30 Hz.
- **Safety Bounds:** Includes velocity clipping to prevent aggressive robot motion.

## Prerequisites
- ROS Noetic / Melodic
- Python 3.8+
- OpenCV (`pip install opencv-python`)
- MediaPipe (`pip install mediapipe`)

## Installation & Usage
1. Clone the repository into your ROS workspace (`catkin_ws/src`):
   ```bash
   cd ~/catkin_ws/src
   git clone [https://github.com/pietrodn06-rbt/ros_mediapipe_teleop.git](https://github.com/pietrodn06-rbt/ros_mediapipe_teleop.git)
