#!/usr/bin/env python3
import cv2
import mediapipe as mp
import rospy
from geometry_msgs.msg import Twist

class GestureTeleopNode:
    def __init__(self):
        rospy.init_node('gesture_teleop_node', anonymous=True)
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.cap = cv2.VideoCapture(0)
        rospy.loginfo("Gesture Teleop Node Started. Controlling via MediaPipe...")

    def run(self):
        rate = rospy.Rate(30) # 30 Hz
        while not rospy.is_shutdown() and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            twist = Twist()

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Track Index Finger Tip (Landmark 8)
                    index_tip = hand_landmarks.landmark[8]
                    cx, cy = int(index_tip.x * w), int(index_tip.y * h)
                    
                    # Normalize coordinates relative to screen center (-1.0 to 1.0)
                    norm_x = (cx - w / 2) / (w / 2)
                    norm_y = (cy - h / 2) / (h / 2)

                    # Map Y movement to linear velocity, X to angular velocity
                    twist.linear.x = -norm_y * 0.5  # Linear speed limit: 0.5 m/s
                    twist.angular.z = -norm_x * 1.0 # Angular speed limit: 1.0 rad/s

                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            self.cmd_pub.publish(twist)
            cv2.imshow("ROS MediaPipe Teleoperation", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            rate.sleep()

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        node = GestureTeleopNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
