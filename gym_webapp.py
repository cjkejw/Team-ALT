import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import bicepcurls_detection, shoulderpress_detection, squats_detection  # Import exercise scripts

st.title("🏋️‍♂️ FormCheck: Your Personal AI-Powered Gym Posture Assistant")

# Open Webcam
cap = cv2.VideoCapture(0)

# Setup Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

stframe = st.empty()  # Placeholder for live video

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Display video
    stframe.image(frame, channels="BGR")
