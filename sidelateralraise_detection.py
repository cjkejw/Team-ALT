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

# Function to track side lateral raises
def lateral_raise_tracker():
    st.subheader("📹 Side Lateral Raise Tracker - Live Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed

    cap = cv2.VideoCapture(0)

    rep_count = 0
    movement_direction = None  # "up" or "down"
    last_angle = 0  # Track the previous arm angle

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

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate arm angles using shoulder as the base
            left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

            # Use the average of both arms for stability
            avg_arm_angle = (left_arm_angle + right_arm_angle) / 2

            # Detect movement direction
            if avg_arm_angle > last_angle + 2:  # Moving up
                movement_direction = "up"
            elif avg_arm_angle < last_angle - 2:  # Moving down
                movement_direction = "down"

            last_angle = avg_arm_angle  # Update last recorded angle

            # Rep Counting Logic
            feedback = "Raise your arms to shoulder height!"
            color = (255, 0, 0)  # Default Red

            # **Step 1**: Arms at rest (below ~20°)
            if avg_arm_angle < 20 and movement_direction == "down":
                arm_down = True  # Confirm arms are fully down

            # **Step 2**: Arms raised to shoulder height (85° to 95°)
            if 85 <= avg_arm_angle <= 95 and movement_direction == "up":
                arm_up = True  # Arms have reached the correct height
                feedback = "Good! Lower now!"
                color = (0, 255, 0)  # Green feedback

            # **Step 3**: Arms return back down (below 20°) → Count rep
            if avg_arm_angle < 20 and arm_up and movement_direction == "down":
                rep_count += 1  # Count rep
                arm_up = False  # Reset for next rep
                feedback = "Good rep! Raise again!"
                color = (0, 255, 0)  # Green feedback

            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Display rep count
            cv2.putText(frame, f"Reps: {rep_count}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Convert frame to RGB before displaying in Streamlit
        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb_display, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
