import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                         min_detection_confidence=0.7, min_tracking_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y, middle_y = 0, 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                #print(x, y)

                # Index
                if id == 8:
                    cv2.circle(frame,(x, y), 10, (0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                # Middle
                if id == 12:
                    cv2.circle(frame,(x, y), 10, (0, 255, 255))
                    middle_x = screen_width/frame_width*x
                    middle_y = screen_height/frame_height*y

                # Thumb
                if id == 4:
                    cv2.circle(frame,(x, y), 5, (255, 0, 0))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    pyautogui.moveTo(thumb_x, thumb_y)
                    if abs(index_y - thumb_y) < 25:
                        print(abs(index_y - thumb_y), ' Click (Left)')
                        pyautogui.leftClick()
                        pyautogui.sleep(1)

                    if abs(middle_y - thumb_y) < 25:
                        print(abs(middle_y - thumb_y), ' Click (Right)')
                        pyautogui.rightClick()
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
