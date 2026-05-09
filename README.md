# Gesture Controlled LED System using Computer Vision

## Overview

This project implements a real-time Gesture Controlled LED System using Computer Vision and Embedded Systems.

The system detects hand gestures using a webcam and controls LEDs connected to an Arduino Uno based on finger movements.

The project integrates:

- OpenCV
- MediaPipe
- Python
- Arduino Uno
- Serial Communication

---

## Features

✅ Real-time hand tracking

✅ Finger state detection

✅ Binary gesture mapping

✅ LED control using gestures

✅ Left and right hand support

✅ Real-time hardware-software interaction

✅ User-friendly graphical interface

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Video processing |
| MediaPipe | Hand landmark detection |
| PySerial | Serial communication |
| Arduino Uno | Hardware control |
| Wokwi | Circuit simulation |
| VS Code | Development environment |

---

## Components Required

| Component | Quantity |
|---|---|
| Arduino Uno | 1 |
| LEDs | 5 |
| 220Ω Resistors | 5 |
| Breadboard | 1 |
| Jumper Wires | Multiple |
| Webcam | 1 |

---

## Working Principle

1. Webcam captures hand gestures.
2. MediaPipe detects hand landmarks.
3. Python identifies open and closed fingers.
4. Finger states are converted into binary commands.
5. Commands are sent to Arduino through serial communication.
6. Arduino controls LEDs based on received commands.

### Example Commands

- `11111` → All LEDs ON
- `00110` → Middle and Ring LEDs ON
- `00000` → All LEDs OFF

---

## System Architecture

```text
Hand Gesture
     ↓
Webcam Input
     ↓
OpenCV Video Processing
     ↓
MediaPipe Hand Tracking
     ↓
Finger Detection Algorithm
     ↓
Binary Command Generation
     ↓
Serial Communication
     ↓
Arduino Uno
     ↓
LED Control
```

---

## Circuit Connections

| LED | Arduino Pin |
|---|---|
| LED 1 | Pin 2 |
| LED 2 | Pin 3 |
| LED 3 | Pin 4 |
| LED 4 | Pin 5 |
| LED 5 | Pin 6 |

All LEDs are connected in series with 220Ω resistors.

Cathodes are connected to GND.

---

## Circuit Diagram

Add your circuit image here:

```markdown
[Circuit Diagram]([circuit_diagram.png](https://github.com/bitcrash79/Gesture-controlled-led-system/blob/main/circuit_diagram.png))
```

---

## Project Screenshots

### All LEDs ON

```markdown
[All LEDs ON](all_leds_on.png)
```

### Right Hand Detection

```markdown
[Right Hand](right_hand_detection.png)
```

### Left Hand Detection

```markdown
[Left Hand](left_hand_detection.png)
```

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/Gesture-Controlled-LED-System.git
```

---

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3: Upload Arduino Code

Upload:

```text
Arduino_Code/sketch.ino
```

to Arduino Uno.

---

### Step 4: Run Python Program

```bash
python Python_Code/hand_tracking.py
```

---

## requirements.txt

```text
opencv-python
mediapipe
pyserial
numpy
```

---

## Future Improvements

- ESP32 wireless control
- Bluetooth integration
- Home automation
- Servo motor control
- Robotic arm control
- IoT integration
- AI gesture classification

---

## Applications

- Smart home automation
- Touchless interfaces
- Human-machine interaction
- Robotics control
- Assistive technologies
- Industrial automation

---

## Demo Video



---

## Author

Kshitija Ingale

---

## License

This project is open-source and available for educational purposes.
