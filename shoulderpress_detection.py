import cv2
import mediapipe as mp
import numpy as np
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Shoulder Press counters
right_press_count = 0
left_press_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert color to RGB for Mediapipe processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    
    # Convert back to BGR for OpenCV display
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Extract landmark positions
        landmarks = results.pose_landmarks.landmark

        # Right Arm Tracking
        right_wrist_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y

        # Detect shoulder press (wrist moves above shoulder)
        if right_wrist_y < right_shoulder_y:
            right_press_count += 1
            right_feedback = "Right OK!"
            right_color = (255, 165, 0)  # Orange
        else:
            right_feedback = "Right Go Higher!"
            right_color = (0, 165, 255)  # Yellow

        cv2.putText(frame, right_feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, right_color, 2)

        # Left Arm Tracking
        left_wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
        left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y

        # Detect shoulder press (wrist moves above shoulder)
        if left_wrist_y < left_shoulder_y:
            left_press_count += 1
            left_feedback = "Left OK!"
            left_color = (255, 165, 0)  # Orange
        else:
            left_feedback = "Left Go Higher!"
            left_color = (0, 165, 255)  # Yellow

        cv2.putText(frame, left_feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, left_color, 2)

        cv2.putText(frame, f"Right Presses: {right_press_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 215, 0), 2)
        cv2.putText(frame, f"Left Presses: {left_press_count}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    cv2.imshow("Shoulder Press Tracker AI", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
