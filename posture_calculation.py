import math
import numpy as np

def calculate_angle(a, b, c):
    """Calculate angle between three points (a, b, c)."""
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point
    c = np.array(c)  # Last point

    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

if results.pose_landmarks:
    landmarks = results.pose_landmarks.landmark

    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    knee_angle = calculate_angle(hip, knee, ankle)

    if knee_angle < 90:
        feedback = "Good squat ✅"
    else:
        feedback = "Go deeper! ❌"

    cv2.putText(frame, feedback, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

