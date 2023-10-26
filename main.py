import cv2
import dlib
import time
from deepface import DeepFace
import subprocess

# set the below to false if not on mac, otherwise running playsound.py will fail.
onmac = True

# Initialize Dlib's face detector
detector = dlib.get_frontal_face_detector()

# Start the video capture
cap = cv2.VideoCapture(0)

# Create and hide the GIF windows on all screens
gif_path = "jumpscare_media/jumpscare.gif"

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

        margin = int(h * 0.1)  # margin calc
        roi_color = frame[max(y-margin, 0):min(y+h+margin, frame.shape[0]),
                          max(x-margin, 0):min(x+w+margin, frame.shape[1])]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        result = DeepFace.analyze(img_path=roi_color, actions=[
                                  'emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        if emotion == "neutral":
            if neutral_start_time is None:
                neutral_start_time = time.time()
            elif time.time() - neutral_start_time >= 15:
                print("Neutral for over 15 seconds!")

                # Show the hidden GIF windows

                # Play the sound
                if onmac:
                    subprocess.Popen(["python3", "showgif.py"])
                    # the below delay is for demo purposes, my computer is too slow to open showgif.py immediatly with playsound.py.
                    time.sleep(2)
                    subprocess.Popen(["python3", "playsound.py"])
                    time.sleep(5)
                else:
                    subprocess.run(["python", "playsound.py"])
                    subprocess.run(["python", "showgif.py"])

                neutral_start_time = None  # reset timer
        else:
            neutral_start_time = None  # reset timer if not neutral

        # Show emotion on frame
        cv2.putText(frame, emotion, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
