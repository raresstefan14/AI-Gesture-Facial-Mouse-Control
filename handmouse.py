import cv2
import mediapipe as mp
import pyautogui
import time

# ---------- MediaPipe Setup ----------
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ---------- Camera ----------
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# ---------- Screen ----------
screen_w, screen_h = pyautogui.size()

# ---------- Cursor smoothing ----------
prev_x, prev_y = 0, 0
smooth = 5

# ---------- Mouth timer ----------
mouth_open_start = None

print("Program started.")
print("Move cursor with index finger.")
print("Pinch index + thumb to click.")
print("Open your mouth for 2 seconds to close the program.")

while True:

    success, img = cap.read()

    if not success:
        print("[ERROR] Cannot read from camera.")
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, c = img.shape

    # ---------- HAND PROCESSING ----------
    results_hands = hands.process(rgb)

    if results_hands.multi_hand_landmarks:

        for handLms in results_hands.multi_hand_landmarks:

            lm_list = []

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if lm_list:

                # index finger
                x, y = lm_list[8]

                # smoothing
                x = prev_x + (x - prev_x) / smooth
                y = prev_y + (y - prev_y) / smooth

                prev_x, prev_y = x, y

                # move mouse
                pyautogui.moveTo(screen_w / w * x, screen_h / h * y)

                # thumb
                x_thumb, y_thumb = lm_list[4]

                # click detection
                if abs(x - x_thumb) < 40 and abs(y - y_thumb) < 40:
                    pyautogui.click()
                    print("Mouse click detected.")
                    time.sleep(0.3)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # ---------- FACE PROCESSING ----------
    results_face = face_mesh.process(rgb)

    if results_face.multi_face_landmarks:

        for faceLms in results_face.multi_face_landmarks:

            # lip landmarks
            upper_lip = faceLms.landmark[13]
            lower_lip = faceLms.landmark[14]

            lip_distance = abs((upper_lip.y - lower_lip.y) * h)

            mouth_threshold = 10

            if lip_distance > mouth_threshold:

                if mouth_open_start is None:
                    mouth_open_start = time.time()

                if time.time() - mouth_open_start > 2:

                    cv2.putText(
                        img,
                        "Mouth open detected. Closing program...",
                        (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

                    cv2.imshow("Hand Mouse", img)
                    cv2.waitKey(1500)

                    print("Mouth open for 2 seconds. Program terminated.")

                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            else:
                mouth_open_start = None

    # ---------- Display ----------
    cv2.imshow("Hand Mouse", img)

    # ESC key exit
    if cv2.waitKey(1) & 0xFF == 27:
        print("ESC pressed. Closing program.")
        break

cap.release()
cv2.destroyAllWindows()