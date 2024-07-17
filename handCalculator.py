import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)

# Gesture definitions
gestures = {
    "zero": [0, 0, 0, 0, 0],
    "one": [0, 1, 0, 0, 0],
    "two": [0, 1, 1, 0, 0],
    "three": [0, 1, 1, 1, 0],
    "four": [0, 1, 1, 1, 1],
    "five": [1, 1, 1, 1, 1],
    "plus": [0, 1, 0, 0, 1],    # Example gesture for "+"
    "minus": [0, 0, 1, 0, 1],   # Example gesture for "-"
    "multiply": [1, 1, 0, 0, 1],# Example gesture for "*"
    "divide": [1, 0, 1, 1, 0],  # Example gesture for "/"
    "equals": [0, 0, 1, 1, 0]   # Example gesture for "="
}

def recognize_gesture(hand_landmarks):
    finger_states = []
    for tip_id in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            finger_states.append(1)
        else:
            finger_states.append(0)
    if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
        finger_states.insert(0, 1)
    else:
        finger_states.insert(0, 0)
    
    for gesture, pattern in gestures.items():
        if finger_states == pattern:
            return gesture
    return None

expression = ""
last_gesture_time = 0
gesture_cooldown = 3.0  # Cooldown period in seconds

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert the image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the RGB image to detect hands
    results = hands.process(img_rgb)
    
    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            current_time = time.time()
            if current_time - last_gesture_time > gesture_cooldown:
                gesture = recognize_gesture(hand_landmarks)
                if gesture:
                    if gesture in ["plus", "minus", "multiply", "divide"]:
                        expression += " " + gesture + " "
                    elif gesture == "equals":
                        try:
                            result = eval(expression.replace("plus", "+").replace("minus", "-").replace("multiply", "*").replace("divide", "/"))
                            expression = str(result)
                        except:
                            expression = "Error"
                    else:
                        expression += gesture.replace("zero", "0").replace("one", "1").replace("two", "2").replace("three", "3").replace("four", "4").replace("five", "5")
                    
                    last_gesture_time = current_time
                    print(f"Gesture: {gesture}, Expression: {expression}")

    # Display the expression on the image
    cv2.putText(img, expression, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3, cv2.LINE_AA)
    
    # Display the image
    cv2.imshow("Hand Gesture Calculator", img)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
