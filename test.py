import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from shoulderpress_detection import shoulder_press_tracker
from squats_detection import squat_tracker
from bicepcurls_detection import bicep_curl_tracker
from wallseat_detection import wall_sit_tracker
from deadlift_detection import deadlift_tracker

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Function to capture and process webcam feed
def exercise_detection():
    st.subheader("📹 Live Webcam Feed")

    cap = cv2.VideoCapture(0)
    stframe = st.empty()  # Placeholder for video feed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture webcam. Please check your camera settings.")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display video feed in Streamlit
        stframe.image(frame, channels="BGR", use_container_width=True)

# Main Streamlit App
st.title("🏋️ Exercise Tracker AI")

# Page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    st.subheader("Select an exercise to track:")

    # Exercise options
    exercise_choice = st.selectbox("Choose an exercise:", 
                                   ["Bicep Curls Detection", "Shoulder Press Detection", "Squats Detection", "Wall Sit Detection", "Deadlift Detection"],
                                   index=None, placeholder="Select an option")

    if exercise_choice:
        if st.button("✅ Confirm"):
            st.session_state["page"] = "exercise"
            st.session_state["exercise"] = exercise_choice
            st.rerun()  # Refresh app state

elif st.session_state["page"] == "exercise":
    st.subheader(f"🏋️ Now Tracking: {st.session_state['exercise']}")
    
    # Back button (outside the while loop)
    if st.button("🔙 Back"):
        st.session_state["page"] = "home"
        st.rerun()  # Refresh app state

    # Call the corresponding function for the selected exercise
    if st.session_state["exercise"] == "Bicep Curls Detection":
        bicep_curl_tracker()
    elif st.session_state["exercise"] == "Shoulder Press Detection":
        shoulder_press_tracker()
    elif st.session_state["exercise"] == "Squats Detection":
        squat_tracker()
    elif st.session_state["exercise"] == "Wall Sit Detection":
        wall_sit_tracker()
    elif st.session_state["exercise"] == "Deadlift Detection":
        deadlift_tracker()
