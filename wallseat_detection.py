import cv2
import mediapipe as mp
import numpy as np
import math
import streamlit as st
import time

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

# Function to track wall sits
def wall_sit_tracker():
    st.subheader("📹 Wall Sit Tracker - Live Webcam Feed")
    stframe = st.empty()  # Placeholder for video feed
    sidebar_placeholder = st.sidebar.empty()  # Sidebar placeholder for clearing old content

    cap = cv2.VideoCapture(0)

    sitting = False
    start_time = 0
    total_time = 0
    set_durations = []  # Stores duration of each set

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

            # Wall sit detection logic
            feedback = "Keep going!"
            color = (0, 0, 255)  # Default Red

            if 80 <= knee_angle <= 100:  # Proper wall sit position
                feedback = "Perfect Wall Sit!"
                color = (0, 255, 0)  # Green

                if not sitting:  # Start a new set
                    sitting = True
                    start_time = time.time()  # Record start time

            else:  # User exits the wall sit position
                feedback = "Not a proper wall sit!"
                color = (0, 0, 255)  # Red

                if sitting:  # End the set
                    sitting = False
                    end_time = time.time()
                    duration = end_time - start_time  # Calculate duration
                    if duration > 2:  # Only count if it's > 2 seconds (to prevent false positives)
                        set_durations.append(int(duration))  # Store duration as an integer
                        total_time += duration

                        # ✅ **Fix Sidebar Duplication Issue**
                        sidebar_placeholder.empty()  # Clear sidebar before updating
                        with sidebar_placeholder:
                            st.sidebar.subheader("📝 Wall Sit Set Summary")
                            for i, dur in enumerate(set_durations, 1):
                                st.sidebar.write(f"Set {i}: {dur} sec")

            cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Display real-time time for current set
            elapsed_time = time.time() - start_time if sitting else 0
            display_time = total_time + elapsed_time

            # Display total session time and sets count
            cv2.putText(frame, f"Session Time: {int(display_time)} sec", (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f"Total Sets: {len(set_durations)}", (50, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Convert frame to RGB before displaying in Streamlit
        frame_rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb_display, channels="RGB", use_container_width=True)

    cap.release()
    cv2.destroyAllWindows()
