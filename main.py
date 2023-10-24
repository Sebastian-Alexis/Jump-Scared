import cv2
from deepface import DeepFace

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 1)
    
    for (x, y, w, h) in faces:
        margin = int(h * 0.1)  # Calculate the margin
        roi_color = frame[max(y-margin, 0):min(y+h+margin, frame.shape[0]), max(x-margin, 0):min(x+w+margin, frame.shape[1])]
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Use DeepFace to predict emotion of the detected face
        result = DeepFace.analyze(img_path=roi_color, actions=['emotion'], enforce_detection=False)
        print(result)  # Add this line to inspect the output
        emotion = result[0]['dominant_emotion']
        
        # Display the emotion on the frame
        cv2.putText(frame, emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Emotion Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
