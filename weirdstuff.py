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

cv2.destroyAllWindows()  # Close any existing OpenCV windows

print("Welcome to Gym Tracker AI!")
print("Select an exercise:")
print("1️. Squats")
print("2️. Bicep Curls")
choice = input("Enter 1 or 2: ")

while True:
    choice = input("Enter 1 or 2: ").strip()
    if choice in ["1", "2"]:
        break
    print("Invalid choice! Please enter 1 or 2.")

exercise = "Squats" if choice == "1" else "Bicep Curls"
print(f"You selected: {exercise}")

cap = cv2.VideoCapture(0)

# Squat counters
squat_count = 0
squat_down = False
standing = True

# Bicep curl counters
curl_count = 0
arm_extended = True

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

        #Squat Tracking (If Selected)
        if exercise == "Squats":
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            knee_angle = calculate_angle(hip, knee, ankle)
            
            # Feedback for squat form
            if knee_angle < 80:
                feedback = "Good squat!"
                color = (0, 255, 0)  # Green
                squat_down = True  # Person is in squat position
            elif knee_angle > 170:
                feedback = "Why are you standing???"
                color = (0, 0, 255)  # Red
            else:
                feedback = "Go further down!"
                color = (0, 165, 255)  # Orange
            
            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Squat repetition counting logic
            if knee_angle > 160:
                standing = True
            
            if knee_angle < 80 and standing:
                squat_count += 1
                squat_down = False
                standing = False
            
            # Display rep count
            cv2.putText(frame, f"Squats: {squat_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Bicep Curl Tracking (If Selected)
        elif exercise == "Bicep Curls":
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            elbow_angle = calculate_angle(shoulder, elbow, wrist)

            # Feedback for bicep curl form
            if elbow_angle > 150:
                curl_feedback = "Arm extended!"
                curl_color = (255, 0, 0)  # Blue
                arm_extended = True
            elif elbow_angle < 50:
                curl_feedback = "Good curl!"
                curl_color = (0, 255, 0)  # Green
            else:
                curl_feedback = "Curl deeper!"
                curl_color = (0, 165, 255)  # Orange

            cv2.putText(frame, curl_feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, curl_color, 2)

            # Bicep curl repetition counting logic
            if elbow_angle > 150:
                arm_extended = True

            if elbow_angle < 50 and arm_extended:
                curl_count += 1
                arm_extended = False

            # Display rep count
            cv2.putText(frame, f"Curls: {curl_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    
    cv2.imshow(f"{exercise} Tracker AI", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()