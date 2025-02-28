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
rep_count = 0
squat_down = False  # Track squat state
standing = True  # Track if the person is fully standing

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
        
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        # Calculate knee angle
        knee_angle = calculate_angle(hip, knee, ankle)
        
        # Squat feedback logic
        if knee_angle < 80:  # More strict squat detection
            feedback = "Good squat!"
            color = (0, 255, 0)  # Green
            squat_down = True  # Person is in squat position
        elif knee_angle > 170:
            feedback = "Why are you standing???"
            color = (255, 165, 0) #Orange
        else:
            feedback = "Go further down!"
            color = (0, 0, 255)  # Red
        
        cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Improved Rep Counting Logic
        if knee_angle > 160:  # Only count rep when person fully stands
            standing = True  # Mark as fully standing
        
        if knee_angle < 80 and standing:  # If person squats after fully standing
            rep_count += 1  # Count rep
            squat_down = False  # Reset squat state
            standing = False  # Reset standing state
        
        # Display rep count
        cv2.putText(frame, f"Reps: {rep_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Show webcam feed
    cv2.imshow("Squat Tracker AI", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()