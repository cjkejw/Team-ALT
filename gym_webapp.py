import streamlit as st
import bicepcurls_detection, shoulderpress_detection, squats_detection  # Import exercise scripts

# Mapping exercises to functions
exercises = {
    "Bicep Curls": bicepcurls_detection.run,
    "Shoulder Press": shoulderpress_detection.run,
    "Squats": squats_detection.run,
}

# Run selected exercise detection
if "selected_exercise" in st.session_state:
    exercise = st.session_state["selected_exercise"]
    st.title(f"🏋️‍♂️ {exercise} Posture Analysis")

    if exercise in exercises:
        exercises[exercise]()  # Call the appropriate function

    if st.button("Back to Main Page"):
        st.session_state["page"] = "main"
        st.rerun()
else:
    st.warning("Please go back and select an exercise first.")


