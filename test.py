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
st.title("🏋️ FormFit")

# Page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if st.session_state["page"] == "home":
    st.markdown("<h2 style='text-align: center;'>Main Menu</h2>", unsafe_allow_html=True)

    # Custom CSS for centering and enlarging buttons
    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            height: 60px;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create two columns for side-by-side buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📷 Example Poses"):
            st.session_state["page"] = "example_poses"
            st.rerun()

    with col2:
        if st.button("🏋️ Select Exercise"):
            st.session_state["page"] = "select_exercise"
            st.rerun()

elif st.session_state["page"] == "example_poses":
    st.subheader("🏋️ Example Poses")

    # Display 5 example images of exercises from the "images" folder
    st.image([
        "images/pose5.jpg", 
        "images/pose2.jpg", 
        "images/pose3.jpg", 
        "images/pose4.jpg", 
        "images/pose1.jpg"
    ], caption=["Bicep Curl Example", "Shoulder Press Example", "Squats Example", "Wall Sit Example", "Deadlift Example"], use_container_width=True)

    # Back button
    if st.button("🔙 Back"):
        st.session_state["page"] = "home"
        st.rerun()

elif st.session_state["page"] == "select_exercise":
    st.subheader("Select an exercise to track:")

    # Exercise options
    exercise_choice = st.selectbox("Choose an exercise:", 
                                   ["Bicep Curls Detection", "Shoulder Press Detection", "Squats Detection", "Wall Sit Detection", "Deadlift Detection"],
                                   index=None, placeholder="Select an option")

    if exercise_choice:
        if st.button("✅ Confirm"):
            st.session_state["page"] = "exercise"
            st.session_state["exercise"] = exercise_choice
            st.rerun()

    # Back button
    if st.button("🔙 Back"):
        st.session_state["page"] = "home"
        st.rerun()

elif st.session_state["page"] == "exercise":
    st.subheader(f"🏋️ Now Tracking: {st.session_state['exercise']}")

    # Back button (outside the while loop)
    if st.button("🔙 Back"):
        st.session_state["page"] = "home"
        st.rerun()

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
