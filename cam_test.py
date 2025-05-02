import cv2
import mediapipe as mp
import pyautogui as pg

from screeninfo import get_monitors

TRACK_IDX = 8
SENSITIVITY = 5

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

last_position = [0, 0]

# Start OpenCV video capture
cap = cv2.VideoCapture(0)  # 0 for default webcam


for m in get_monitors():
    frame_width = m.width
    frame_height = m.height

cursor_position = (frame_width // 2, frame_height// 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    

    # Convert frame to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand tracking
    results = hands.process(rgb_frame)

    # Draw landmarks if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            #print(hand_landmarks)
        
        # print(min(frame_width, (1-results.multi_hand_landmarks[0].landmark[TRACK_IDX].x) * frame_width * SENSITIVITY), 
        #           min(frame_height, results.multi_hand_landmarks[0].landmark[TRACK_IDX].y * frame_height * SENSITIVITY))
        curr_pos = [(1-results.multi_hand_landmarks[0].landmark[TRACK_IDX].x) * frame_width, 
                         results.multi_hand_landmarks[0].landmark[TRACK_IDX].y * frame_height]
        movement = [(last_position[0] - curr_pos[0]) * SENSITIVITY, (last_position[1] - curr_pos[1]) * SENSITIVITY]
        cursor_position = [max(5, min(frame_width - 5, cursor_position[0] + movement[0])), max(5, min(frame_height - 5, cursor_position[1] - movement[1]))]
        last_position = curr_pos.copy()

        print(cursor_position)
        pg.moveTo(cursor_position[0], cursor_position[1], 0.01)
    # Show the frame
    cv2.imshow("MediaPipe Hand Tracking", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
