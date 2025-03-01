import streamlit as st
import subprocess

def run_script(script_name):
    """Runs the selected exercise detection script."""
    process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

st.title("🏋️ Exercise Tracker AI")

st.write("Select an exercise detection script to run:")

# Exercise options
scripts = {
    "Bicep Curls Detection": "bicepcurls_detection.py",
    "Shoulder Press Detection": "shoulderpress_detection.py",
    "Squats Detection": "squats_detection.py"
}

# Create a selection box
exercise_choice = st.selectbox("Choose an exercise:", list(scripts.keys()), index=None, placeholder="Select an option")

# Run the selected script when button is clicked
if exercise_choice:
    if st.button(f"Run {exercise_choice}"):
        st.write(f"Running {exercise_choice}...")

        # Run the selected script in the background
        process = run_script(scripts[exercise_choice])

        # Display output logs
        with st.expander(f"Output of {exercise_choice}"):
            stdout, stderr = process.communicate()
            st.text(stdout.decode("utf-8"))
            if stderr:
                st.text("Errors:\n" + stderr.decode("utf-8"))
