import streamlit as st
import bicepcurls_detection, shoulderpress_detection, squats_detection  # Import exercise scripts

st.title("🏋️‍♂️ FormCheck: Your Personal AI-Powered Gym Posture Assistant")
st.write("## Welcome to FormCheck, your personal AI-Powered Gym Posture Assistant to help check your posture whenever needed!")

st.write("## What is this about?")
st.write("## What we do")

# Dropdown menu to select exercise
exercise = st.selectbox("Choose an exercise to analyze:", 
                         ["Select an exercise", "Bicep Curls", "Shoulder Press", "Squats"])

# Confirm button
if st.button("Confirm"):
    if exercise == "Bicep Curls":
        bicepcurls_detection.run()  # Call the function from bicepcurls_detection.py
    elif exercise == "Shoulder Press":
        shoulderpress_detection.run()  # Call the function from shoulderpress_detection.py
    elif exercise == "Squats":
        squats_detection.run()  # Call the function from squats_detection.py
    else:
        st.warning("Please select an exercise before confirming.")
