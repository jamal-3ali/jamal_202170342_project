import cv2
import pygame
import threading

# Initialize pygame mixer
pygame.mixer.init()

# Load your sound file
pygame.mixer.music.load('audio.mp3')  # Replace with your audio file path

# Load the pre-trained fire detection model
fire_cascade = cv2.CascadeClassifier('fire_detection.xml')

# Start video capture (0 for webcam, or you can use a video file)
cap = cv2.VideoCapture(0)

def play_sound():
    pygame.mixer.music.play()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect fire
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    # Check if fire is detected
    fire_detected = False
    for (x, y, w, h) in fire:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        fire_detected = True
        print('Fire is detected!')
        
        # Play sound in a separate thread
        threading.Thread(target=play_sound).start()

        # Draw a rectangle around the detected fire
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the current frame
    cv2.imshow('Fire Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()