import cv2
import dlib
import time
from deepface import DeepFace
import subprocess

# Set the below to false if not on mac, otherwise running playsound.py will fail.
onmac = True


# Initialize Dlib's face detector
detector = dlib.get_frontal_face_detector()

# Start the video capture
cap = cv2.VideoCapture(0)

neutral_start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame using Dlib
    faces = detector(gray)

    for rect in faces:
        x = rect.left()
        y = rect.top()
        w = rect.width()
        h = rect.height()

        margin = int(h * 0.1)  # Calculate the margin
        roi_color = frame[max(y-margin, 0):min(y+h+margin, frame.shape[0]),
                          max(x-margin, 0):min(x+w+margin, frame.shape[1])]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        result = DeepFace.analyze(img_path=roi_color, actions=[
                                  'emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        # Check if emotion is neutral
        if emotion == "neutral":
            if neutral_start_time is None:
                neutral_start_time = time.time()
            elif time.time() - neutral_start_time >= 15:
                print("User has been neutral for over 15 seconds!")

                # Call the playsound.py script
                if onmac == True:
                    subprocess.run(
                        ["python3", "showgif.py"])

                    subprocess.run(
                        ["python3", "playsound.py"])

                else:
                    subprocess.run(
                        ["python", "playsound.py"])
                    subprocess.run(
                        ["python", "playsound.py"])
                # Reset the timer
                neutral_start_time = None

        # Display the emotion on the frame
        cv2.putText(frame, emotion, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
