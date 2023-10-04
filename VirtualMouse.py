import cv2
import numpy as np
import time
import pyautogui
import HandTrackingModule as htm

############
wCam, hCam = 640, 480
frameR = 80
smoothening = 2
MirrorCamera = True
############

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
wScr, hScr = pyautogui.size()
detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    if MirrorCamera:
        img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    cv2.rectangle(
        img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2
    )

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()

        # Index finger up
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.putText(
                img,
                f"Mode: Move",
                (10, hCam - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        # Index & Middle fingers up
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img, True, 8)
            cv2.putText(
                img,
                f"Mode: Click",
                (10, hCam - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            # print(length)

            if fingers[4] == 0 and length < 25:  # Left Click
                print(length, " Left Click")
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 8, (0, 255, 0), cv2.FILLED)
                pyautogui.leftClick()
                pyautogui.sleep(1)
            elif fingers[4] == 1 and length < 25:  # Right Click
                print(length, " Right Click")
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 8, (0, 255, 0), cv2.FILLED)
                pyautogui.rightClick()
                pyautogui.sleep(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (5, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
