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
```
## 🔐 **Security Features**

- **Password login system**
- **Email alerts** sent after multiple failed login attempts
- Plays **video** or shows **image** based on login **success/failure**

---

## 🔌 **Arduino Communication**

Uses **serial module** (`pyserial`) to send and receive commands between Python and Arduino.

### 📡 **Example Commands**

- `s1.write(b"e")` → Open garage door  
- `s1.write(b"g")` → Close garage door  
- `s1.write(b"n")` → Request temperature reading from Arduino

---

## 🌡️ **Real-Time Temperature Update**

- Uses `Tkinter.after()` to periodically request temperature from Arduino  
- Temperature is displayed in the **GUI** using a `Label`

---

## 🔙 **Return to Main Menu**

- A **"Back" button** destroys the current frame and reloads the main interface (`Host.py`)

---

## 📁 **Recommended Project Structure**
SmartHome/
├── images/
│ ├── sim.jpg
│ ├── new_sim.jpg
│ ├── door.jpg
│ └── ...
├── music/
│ ├── opn.mp3
│ └── ...
├── Host.py
├── control_panel.py
├── garage.py
├── README.md
└── requirements.txt

---

## ▶️ **How to Run**

### 1. **Install dependencies**:

```bash
pip install pillow pygame pyserial
```
### 2. Run the main program:
```bash
python Host.py
```
---

## 💡 **Future Ideas**
Add RGB light control interface

Add remote control support via web or mobile app

Log user access and control history

