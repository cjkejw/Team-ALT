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

# Function to track squats
def squat_tracker():
    st.subheader("📹 Squat Tracker - Live Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed

    cap = cv2.VideoCapture(0)

    rep_count = 0
    squat_down = False
    standing = True

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

            # Extract landmark positions
            landmarks = results.pose_landmarks.landmark

            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            knee_angle = calculate_angle(hip, knee, ankle)

            # Squat detection logic
            feedback = "Keep going!"
            color = (0, 0, 255)  # Default Red

            if knee_angle < 80:  # Proper squat depth
                feedback = "Good squat!"
                color = (0, 255, 0)  # Green
                squat_down = True
            elif knee_angle > 170:
                feedback = "Why are you standing???"
                color = (255, 165, 0)  # Orange
            else:
                feedback = "Go further down!"
                color = (0, 0, 255)  # Red

            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Count squats
            if knee_angle > 160:  # Only count rep when person fully stands
                standing = True  

            if knee_angle < 80 and standing:  # If person squats after fully standing
                rep_count += 1
                squat_down = False
                standing = False

            # Display rep count
            cv2.putText(frame, f"Reps: {rep_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Convert frame to RGB before displaying in Streamlit
        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb_display, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
