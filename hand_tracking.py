import cv2
import mediapipe as mp
import serial
import time
from collections import deque

# ─── Connect to Wokwi via RFC2217 ─────────────────────────────────────────────
print("Connecting to Wokwi simulator...", flush=True)
try:
    ser = serial.serial_for_url('rfc2217://localhost:4000', baudrate=9600, timeout=1)
    print("Connected to Wokwi!", flush=True)
except Exception as e:
    print(f"Could not connect: {e}", flush=True)
    print("Make sure Wokwi simulator is running first!", flush=True)
    exit()

# ─── MediaPipe Setup ───────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

# ─── Webcam ───────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ─── Stability Buffer ─────────────────────────────────────────────────────────
buffers = [deque(maxlen=7) for _ in range(5)]

# ─── Detect individual fingers ────────────────────────────────────────────────
def get_finger_states(lm, hand_label):
    """
    Returns [thumb, index, middle, ring, pinky] True/False
    Since frame is flipped, thumb logic is reversed from normal
    """
    states = [False] * 5

    # Thumb — FIXED: reversed because we flip the frame
    if hand_label == "Right":
        states[0] = lm.landmark[4].x < lm.landmark[3].x
    else:  # Left
        states[0] = lm.landmark[4].x > lm.landmark[3].x

    # Index, Middle, Ring, Pinky
    tips = [8,  12, 16, 20]
    pips = [6,  10, 14, 18]
    for i, (tip, pip) in enumerate(zip(tips, pips)):
        states[i + 1] = lm.landmark[tip].y < lm.landmark[pip].y

    return states

# ─── LED Colors ───────────────────────────────────────────────────────────────
FINGER_NAMES  = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
LED_COLORS_ON = [(0,100,255),(0,220,100),(255,200,0),(255,120,0),(255,60,60)]
LED_COLOR_OFF = (40, 40, 40)

# ─── Draw LED panel ───────────────────────────────────────────────────────────
def draw_leds(frame, cmd):
    h, w = frame.shape[:2]
    if len(cmd) != 5:
        return
    for i in range(5):
        cx = w - 220 + i * 45
        cy = 55
        is_on = cmd[i] == "1"
        color = LED_COLORS_ON[i] if is_on else LED_COLOR_OFF
        if is_on:
            cv2.circle(frame, (cx, cy), 20, tuple(min(255, c+60) for c in color), -1)
        cv2.circle(frame, (cx, cy), 14, color, -1)
        cv2.circle(frame, (cx, cy), 14, (200, 200, 200), 1)
        cv2.putText(frame, f"L{i+1}", (cx-12, cy+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200,200,200), 1)

# ─── Main Loop ────────────────────────────────────────────────────────────────
last_cmd      = "00000"
last_time     = time.time()
DEBOUNCE      = 0.1
stable_states = [False] * 5
current_hand  = "Right"

print("=== Finger-to-LED Controller ===")
print("RIGHT hand: Thumb=LED5(pin6) ... Pinky=LED1(pin2)")
print("LEFT  hand: Thumb=LED1(pin2) ... Pinky=LED5(pin6)")
print("Press Q to quit.")

# Send initial command to make sure Arduino is ready
time.sleep(1)
ser.write(b"00000\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame  = cv2.flip(frame, 1)
    rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_states = [False] * 5
    hand_detected  = False

    if result.multi_hand_landmarks:
        for hand_lm, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
            current_hand  = hand_info.classification[0].label
            hand_detected = True

            mp_draw.draw_landmarks(
                frame, hand_lm,
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )
            current_states = get_finger_states(hand_lm, current_hand)

    # Stability buffer — vote per finger
    for i in range(5):
        buffers[i].append(current_states[i])
        stable_states[i] = buffers[i].count(True) > len(buffers[i]) // 2

    # Build command string [thumb, index, middle, ring, pinky]
    cmd_list = ["1" if s else "0" for s in stable_states]

    # Right hand → reverse (thumb=LED5, pinky=LED1)
    # Left hand  → normal  (thumb=LED1, pinky=LED5)
    if current_hand == "Right":
        cmd_list = cmd_list[::-1]

    cmd = "".join(cmd_list)

    # Send to Wokwi only when changed
    now = time.time()
    if cmd != last_cmd and (now - last_time) > DEBOUNCE:
        try:
            ser.write((cmd + "\n").encode())
            active = [FINGER_NAMES[i] for i in range(5) if stable_states[i]]
            print(f"Hand: {current_hand} | CMD: {cmd} | UP: {', '.join(active) if active else 'None'}", flush=True)
            last_cmd  = cmd
            last_time = now
        except Exception as e:
            print(f"Serial error: {e}", flush=True)

    # ── UI Overlay ────────────────────────────────────────────────────────
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (640, 95), (10, 10, 10), -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    active_names = [FINGER_NAMES[i] for i in range(5) if stable_states[i]]
    status_text  = ", ".join(active_names) if active_names else "No fingers up"
    hand_color   = (0, 255, 100) if hand_detected else (100, 100, 100)
    hand_text    = f"{current_hand} Hand" if hand_detected else "NO HAND"

    cv2.putText(frame, hand_text, (15, 30),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, hand_color, 2)
    cv2.putText(frame, status_text, (15, 58),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 220, 0), 1)
    cv2.putText(frame, f"CMD: {last_cmd}", (15, 82),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
    cv2.putText(frame, "Press Q to quit", (450, 82),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (120, 120, 120), 1)

    draw_leds(frame, last_cmd)
    cv2.imshow("Finger LED Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
try:
    ser.write(b"00000\n")
    ser.close()
except:
    pass

cap.release()
cv2.destroyAllWindows()
print("Stopped. All LEDs OFF.")