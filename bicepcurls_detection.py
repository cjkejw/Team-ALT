import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)
    
    return 360 - angle if angle > 180 else angle

# Open webcam
cap = cv2.VideoCapture(0)

# Bicep Curl counters for both arms
right_curl_count = 0
right_arm_extended = True
left_curl_count = 0
left_arm_extended = True

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
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        # Feedback for right bicep curl form
        if right_elbow_angle > 150:
            right_curl_feedback = "Right Arm Extended!"
            right_curl_color = (255, 0, 0)  # Blue
            right_arm_extended = True
        elif right_elbow_angle < 50:
            right_curl_feedback = "Good Right Curl!"
            right_curl_color = (0, 255, 0)  # Green
        else:
            right_curl_feedback = "Curl More!"
            right_curl_color = (0, 165, 255)  # Orange

        cv2.putText(frame, right_curl_feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, right_curl_color, 2)

        # Right bicep curl repetition counting logic
        if right_elbow_angle > 150:
            right_arm_extended = True

        if right_elbow_angle < 50 and right_arm_extended:
            right_curl_count += 1
            right_arm_extended = False

        # Left Arm Tracking
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

        # Feedback for left bicep curl form
        if left_elbow_angle > 150:
            left_curl_feedback = "Left Arm Extended!"
            left_curl_color = (255, 0, 0)  # Blue
            left_arm_extended = True
        elif left_elbow_angle < 50:
            left_curl_feedback = "Good Left Curl!"
            left_curl_color = (0, 255, 0)  # Green
        else:
            left_curl_feedback = "Curl More!"
            left_curl_color = (0, 165, 255)  # Orange

        cv2.putText(frame, left_curl_feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, left_curl_color, 2)

        # Left bicep curl repetition counting logic
        if left_elbow_angle > 150:
            left_arm_extended = True

        if left_elbow_angle < 50 and left_arm_extended:
            left_curl_count += 1
            left_arm_extended = False

        cv2.putText(frame, f"Right Curls: {right_curl_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, f"Left Curls: {left_curl_count}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    cv2.imshow("Bicep Curl Tracker AI (Both Arms)", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
