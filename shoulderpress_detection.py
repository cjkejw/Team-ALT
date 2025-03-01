import cv2
import mediapipe as mp
import numpy as np
import math
import streamlit as st

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

# Function to track shoulder press
def shoulder_press_tracker():
    st.subheader("📹 Shoulder Press Tracker - Live Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed

    cap = cv2.VideoCapture(0)

    rep_count = 0
    arms_down = False  # Initially, the arms are up

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture webcam. Please check your camera settings.")
            break
        
        frame = cv2.flip(frame, 1)  # Flip for natural webcam view
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract landmarks for shoulder, elbow, and wrist
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            # Shoulder press detection logic
            feedback = "Keep going!"
            color = (0, 0, 255)  # Default Red

            if angle > 160:  # Arms fully extended (up)
                feedback = "Arms Are Up!"
                color = (0, 255, 0)  # Green
                arms_down = False
            elif angle < 70:  # Arms fully down (lowered)
                feedback = "Push Up!"
                color = (255, 165, 0)  # Orange
                if not arms_down:
                    rep_count += 1  # Count rep when arms go fully down
                    arms_down = True
            elif angle > 90 and angle < 160:  # In neutral position (shoulder press)
                feedback = "Go Up!"
                color = (255, 255, 0)  # Yellow (Neutral)

            # Display feedback text
            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Display rep count
            cv2.putText(frame, f"Reps: {rep_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Convert frame to RGB before displaying in Streamlit
        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb_display, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
