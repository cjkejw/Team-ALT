import streamlit as st
import subprocess

# Exercise script mapping
exercises = {
    "Bicep Curls": "bicepcurls_detection.py",
    "Shoulder Press": "shoulderpress_detection.py",
    "Squats": "squats_detection.py",
}

# Streamlit UI
st.title("🏋️‍♂️ FormCheck: AI-Powered Gym Posture Assistant")

exercise = st.selectbox("Choose an exercise:", ["Select an exercise"] + list(exercises.keys()))

if st.button("Confirm"):
    if exercise != "Select an exercise":
        st.write(f"Launching {exercise} detection...")

        # Run the script as a separate process
        subprocess.run(["python", exercises[exercise]])
