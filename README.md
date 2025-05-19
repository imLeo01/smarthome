# 🏠 SmartHome - Python Tkinter GUI Project

## 📌 Project Description
**SmartHome** is a Python GUI application built using `Tkinter` that simulates and controls a smart home system. The interface supports:
- Password-based login
- Device control (lights, doors, garage)
- Real-time temperature monitoring from Arduino
- Music playback with theme-based UI switching
- Dynamic background and button image updates based on selected song

---

## 🧰 Technologies Used
- `Python 3.x`
- `Tkinter` - for GUI
- `Pillow (PIL)` - for image processing
- `Pygame` - for music playback
- `PySerial` - for serial communication with Arduino

---

## 🖼️ Main Interface

- **Control Panel**: Main screen for controlling rooms like bedroom, living room, garage, etc.
- **Garage Interface**: Dedicated screen for garage door control, real-time temperature, and music control.
- **Dynamic UI Switching**: Background and button images change based on selected song.

---

## 🎵 Music & UI Theme System
- UI themes are defined per song using dictionaries:

```python
background_images_control_panel = {
    "Song 1": "path/to/background1.jpg",
    "Song 2": "path/to/background2.jpg",
    ...
}

button_images_control_panel = {
    "Song 1": {
        "hjhj": "sim.jpg",
        "sd": "shit.jpg",
        ...
    },
    "Song 2": {
        "hjhj": "new_sim.jpg",
        "sd": "new_shit.jpg",
        ...
    }
}

When a song is selected:

Music plays using pygame

Background and control button images are updated to match the selected theme

## 🔐 Security Features
Password login system

Sends email alert after multiple failed login attempts

Plays video or shows image based on login success/failure

## 🔌 Arduino Communication
Uses serial module to send/receive commands to Arduino

Examples:

s1.write(b"e"): Open garage door

s1.write(b"g"): Close garage door

s1.write(b"n"): Request temperature reading from Arduino

## 🌡️ Real-Time Temperature Update
Uses Tkinter.after() to periodically request and display temperature data from Arduino

Temperature is shown on the GUI via a Label

## 🔙 Return to Main Menu
"Back" button destroys the current frame and loads the main Host.py interface

## 📁 Recommended Project Structure
SmartHome/
├── images/
│   ├── sim.jpg
│   ├── new_sim.jpg
│   ├── door.jpg
│   └── ...
├── music/
│   ├── opn.mp3
│   └── ...
├── Host.py
├── control_panel.py
├── garage.py
├── README.md
└── requirements.txt
## ▶️ How to Run
Install required packages:

bash
pip install pillow pygame pyserial
Run the main program:

bash
python Host.py

##💡 Future Ideas
Add RGB light control interface

Add remote control support via web or mobile app

Log user access and control history

