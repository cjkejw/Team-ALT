import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Shoulder Press counters
right_press_count = 0
left_press_count = 0
right_press_up = False
left_press_up = False

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)

    return 360 - angle if angle > 180 else angle

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

        # Right arm tracking
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Start position: Elbow at ~90 degrees
        if 80 <= right_elbow_angle <= 100:
            right_press_up = False  # Ready to count the next press
        
        # Press position: Arm extended (elbow ~155 degrees)
        if 150 <= right_elbow_angle <= 165 and not right_press_up:
            right_press_count += 1
            right_press_up = True  # Count press only once per rep

        # Feedback for right arm
        right_feedback = "Right Press OK!" if right_press_up else "Start from 90 degrees!"
        right_color = (0, 255, 0) if right_press_up else (0, 165, 255)  # Green for full press, Yellow otherwise
        cv2.putText(frame, right_feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, right_color, 2)

        # Left arm tracking
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Start position: Elbow at ~90 degrees
        if 80 <= left_elbow_angle <= 100:
            left_press_up = False  # Ready to count the next press

        # Press position: Arm extended (elbow ~155 degrees)
        if 150 <= left_elbow_angle <= 165 and not left_press_up:
            left_press_count += 1
            left_press_up = True  # Count press only once per rep

        # Feedback for left arm
        left_feedback = "Left Press OK!" if left_press_up else "Start from 90 degrees!"
        left_color = (0, 255, 0) if left_press_up else (0, 165, 255)  # Green for full press, Yellow otherwise
        cv2.putText(frame, left_feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, left_color, 2)

        cv2.putText(frame, f"Right Presses: {right_press_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 215, 0), 2)
        cv2.putText(frame, f"Left Presses: {left_press_count}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    cv2.imshow("Shoulder Press Tracker AI", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
