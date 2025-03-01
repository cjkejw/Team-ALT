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

# Function to track deadlifts
def deadlift_tracker():
    st.subheader("📹 Deadlift Tracker - Live Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed

    cap = cv2.VideoCapture(0)

    rep_count = 0
    bar_down = True  # Ensures rep starts with the bar lowered

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

            # Key points for deadlift
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,  # Fixed elbow definition
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            knee_angle = calculate_angle(hip, knee, ankle)
            arm_angle = calculate_angle(shoulder, elbow, wrist)  # Ensure arms stay straight

            # Deadlift detection logic
            feedback = "Lower the bar and maintain form!"
            color = (0, 0, 255)  # Default Red

            # Ensure arms stay straight
            if arm_angle < 170:
                feedback = "Keep your arms straight!"
                color = (0, 0, 255)  # Red warning

            elif knee_angle > 160 and bar_down:  # Fully extended (lockout position)
                feedback = "Good lockout! Lower now."
                color = (0, 255, 0)  # Green
                bar_down = False  # Rep is in upward phase

            elif knee_angle < 110 and not bar_down:  # Lowered back down
                rep_count += 1
                feedback = "Good rep! Lift again."
                bar_down = True  # Reset for next rep
                color = (0, 255, 0)  # Green feedback

            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Display rep count
            cv2.putText(frame, f"Reps: {rep_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Convert frame to RGB before displaying in Streamlit
        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb_display, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
