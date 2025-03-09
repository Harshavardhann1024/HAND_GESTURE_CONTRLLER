# Hand Gesture Controlled LED System

A real-time hand gesture recognition system that uses MediaPipe Hands and OpenCV to control LEDs connected to an Arduino. This project is designed to assist home-sick patients by providing an easy way to control devices using simple hand gestures.

## 🚀 Features
- Real-time hand landmark detection using **MediaPipe Hands**.
- Virtual button interface for seamless LED control.
- Arduino integration via **pyFirmata** for hardware control.
- Visual (LED) and auditory (buzzer) feedback for enhanced accessibility.
- Designed to be simple yet effective for home-sick patient monitoring.

## 🛠️ Requirements
Ensure you have the following dependencies installed:

```
opencv-python
mediapipe
pyfirmata
```

Install these libraries using the command:
```
pip install opencv-python mediapipe pyfirmata
```

## 📋 Installation
1. Clone this repository:
   ```
   git clone https://github.com/Harshavardhann1024/HAND_GESTURE_CONROLLER.git
   ```
2. Navigate to the project folder:
   ```
   cd HAND_GESTURE_CONTROLLER
   ```
3. Connect your **Arduino** to your computer via USB.
4. Update the port in `gesture_controller.py` (e.g., `'COM3'`).
5. Run the program:
   ```
   python.py
   ```

## 🖐️ How It Works
1. The system tracks your hand in real-time using **MediaPipe Hands**.
2. The index finger's tip is mapped to interactive virtual buttons on the screen.
3. Moving your fingertip into a button area toggles the corresponding LED on or off.

## 🎯 Virtual Button Controls
- **LED 1** → Top-left button
- **LED 2** → Top-middle button
- **LED 3** → Top-right button
- **LED 4** → Far-right button

## 📚 Future Improvements
- Add multi-hand support.
- Implement gesture-based motor speed and direction control.
- Enhance button accuracy with improved detection logic.

## 🤝 Contribution
Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

## 📧 Contact
If you have any questions or feedback, please reach out at youcan24261024@gmail.com.

