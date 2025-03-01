import streamlit as st

# Import detection modules
import bicepcurls_detection
import shoulderpress_detection
import squats_detection

# Exercise options
exercises = {
    "Bicep Curls": bicepcurls_detection.run,
    "Shoulder Press": shoulderpress_detection.run,
    "Squats": squats_detection.run,
}

# Main page UI
st.title("🏋️‍♂️ FormCheck: AI-Powered Gym Posture Assistant")

exercise = st.selectbox("Choose an exercise to analyze:", ["Select an exercise"] + list(exercises.keys()))

if st.button("Confirm"):
    if exercise != "Select an exercise":
        st.session_state["selected_exercise"] = exercise
        st.session_state["page"] = "exercise"
        st.rerun()
    else:
        st.warning("Please select an exercise before confirming.")
