# 🏠 SmartHome - Python Tkinter GUI Project

## 📌 Description
**SmartHome** is a desktop application built with Python and Tkinter that simulates a smart home control system. It allows users to interact with home components such as doors, lights, music, and temperature monitoring through an interactive GUI.

---

## 🧰 Technologies Used

- Python 3.x
- Tkinter – for GUI
- Pillow (PIL) – image processing
- Pygame – music playback
- PySerial – serial communication with Arduino

---

## 🖼️ Features

### 🔐 Login System
- Password-protected access
- Plays a video if login is successful
- Displays an alert image if multiple failed login attempts
- Sends email notification on failed login attempts

### 🕹️ Control Panel
- Control buttons for: bedroom, living room, garage, and doors
- Buttons are image-based and change appearance depending on the selected music/theme

### 🖌️ Dynamic UI Switching
- Each music selection comes with its own theme:
  - Background image
  - Button images (bedroom, garage, lights, etc.)

```python
background_images_control_panel = {
    "Song 1": "background1.jpg",
    "Song 2": "background2.jpg"
}

button_images_control_panel = {
    "Song 1": {
        "bedroom": "bedroom.jpg",
        "garage": "garage.jpg",
        ...
    },
    "Song 2": {
        "bedroom": "new_bedroom.jpg",
        "garage": "new_garage.jpg",
        ...
    }
}
