🔐 Security Features
Password login system

Sends email alert after multiple failed login attempts

Plays video or shows image based on login success/failure

🔌 Arduino Communication
Uses serial module to send/receive commands to Arduino

Examples:

s1.write(b"e"): Open garage door

s1.write(b"g"): Close garage door

s1.write(b"n"): Request temperature reading from Arduino

🌡️ Real-Time Temperature Update
Uses Tkinter.after() to periodically request and display temperature data from Arduino

Temperature is shown on the GUI via a Label

🔙 Return to Main Menu
"Back" button destroys the current frame and loads the main Host.py interface

📁 Recommended Project Structure
Sao chép
Chỉnh sửa
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

▶️ How to Run
Install required packages:
pip install pillow pygame pyserial
Run the main program:
python Host.py

💡 Future Ideas
Add RGB light control interface

Add remote control support via web or mobile app

Log user access and control history
