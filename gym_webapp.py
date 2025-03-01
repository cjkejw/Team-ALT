# app.py (Streamlit Web App)

import streamlit as st
import cv2
import bicepcurls_detection, shoulderpress_detection, squats_detection

# Web page setup
st.title("🏋️‍♂️ FormCheck: AI-Powered Gym Posture Assistant")

# Start webcam
stframe = st.empty()  # Placeholder for live video

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame with PoseDetection
    frame = pose_detector.process_frame(frame)

    # Display processed frame in Streamlit
    stframe.image(frame, channels="BGR")

# Release pose detection resources
pose_detector.release()

cap.release()
