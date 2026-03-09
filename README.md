# AI-Gesture-Facial-Mouse-Control
This project transforms your webcam into a smart mouse using Computer Vision to control the cursor via hand gestures and execute commands (like closing the program) through facial movements.

🚀 Features
Cursor Control: Move the system mouse smoothly by pointing with your index finger.

Intelligent Click: Pinch detection (joining thumb and index finger) to trigger a left click.

Mouth-Command Exit: Secure application shutdown by holding your mouth open for 2 seconds (prevents accidental closings).

Cursor Smoothing: Implemented a smoothing algorithm to eliminate jitter and provide a fluid user experience.

Live Feedback: Real-time on-screen display of lip distance and the countdown timer for closing the app.

🛠️ Built With
OpenCV: For video stream capturing and frame processing.

MediaPipe: For high-fidelity hand and face landmark detection.

PyAutoGUI: For direct interaction with the OS-level cursor and mouse events.

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/raresstefan14/AI-Mouse-Control.git
cd AI-Mouse-Control
Install the required dependencies:

Bash
pip install opencv-python mediapipe pyautogui
Run the application:

Bash
python main.py
🎮 How to Use
Navigation: Raise your hand and move your index finger to move the cursor.

Clicking: Pinch your thumb and index finger together.

Closing the App: Open your mouth wide for 2 seconds or press the ESC key.

⭐ Developed by raresstefan14
