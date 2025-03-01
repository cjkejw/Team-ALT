import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

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
                                   ["Bicep Curls Detection", "Shoulder Press Detection", "Squats Detection"],
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

    # Run the exercise detection
    exercise_detection()
