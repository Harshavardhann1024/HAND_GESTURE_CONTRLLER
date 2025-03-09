import cv2
import mediapipe as mp
from pyfirmata import Arduino, util
import time

# Connect to the Arduino
board = Arduino('COM3')  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Allow time for the connection to establish

# Define LED pins
led_pins = [2, 3, 4, 5]  # LEDs connected to these pins on the Arduino

# Set up pins as OUTPUT
for pin in led_pins:
    board.digital[pin].mode = 1  # 1 means OUTPUT mode

# OpenCV setup
cap = cv2.VideoCapture(0)
wCam, hCam = 640, 480
cap.set(3, wCam)
cap.set(4, hCam)

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,  # Detect only one hand for better performance
    min_detection_confidence=0.8,  # Increased for better accuracy
    min_tracking_confidence=0.8  # Increased for better tracking stability
)
mp_draw = mp.solutions.drawing_utils

# Define virtual button areas and labels
buttons = [
    {"coords": ((50, 100), (150, 200)), "label": "LED 1"},
    {"coords": ((200, 100), (300, 200)), "label": "LED 2"},
    {"coords": ((350, 100), (450, 200)), "label": "LED 3"},
    {"coords": ((500, 100), (600, 200)), "label": "LED 4"},
]

button_states = [False, False, False, False]  # Initial states of LEDs
last_toggle_time = [0, 0, 0, 0]  # Store last toggle time for each button
delay_time = 0.5  # Delay in seconds


def draw_buttons(frame):
    """Draw virtual buttons on the frame."""
    for i, button in enumerate(buttons):
        x1, y1 = button["coords"][0]
        x2, y2 = button["coords"][1]
        color = (0, 255, 0) if button_states[i] else (0, 0, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.putText(frame, button["label"], (x1 + 20, y1 + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally for easier control
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    result = hands.process(rgb_frame)

    # Pre-process the frame for better accuracy
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contrast_frame = cv2.equalizeHist(gray_frame)

    # Draw buttons on the frame
    draw_buttons(frame)

    # Check for hand interaction with buttons
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get fingertip coordinates (index finger tip - landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            x = int(index_finger_tip.x * wCam)
            y = int(index_finger_tip.y * hCam)

            # Check if fingertip is within any button
            for i, button in enumerate(buttons):
                x1, y1 = button["coords"][0]
                x2, y2 = button["coords"][1]

                if x1 < x < x2 and y1 < y < y2:
                    current_time = time.time()
                    if current_time - last_toggle_time[i] > delay_time:
                        button_states[i] = not button_states[i]
                        board.digital[led_pins[i]].write(1 if button_states[i] else 0)
                        last_toggle_time[i] = current_time  # Update last toggle time

    # Display the frame
    cv2.putText(frame, "Press Q to Quit", (10, hCam - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Virtual Button Controller", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
board.exit()