🎵 Music Control
Select music with radio buttons

Music starts automatically and loops

Each song changes the theme of the interface

🚪 Garage & Door Control
Open/close garage door via serial commands:

s1.write(b"e") → Open

s1.write(b"g") → Close

Toggle house main door with similar commands

Buttons update their image based on door state

🌡️ Temperature Monitoring
Reads temperature from Arduino every second

Displays live temperature in the GUI

🔁 Return to Main Menu
A back button to return from garage screen to main control panel (Host.py)

🔌 Arduino Integration
Communicates via Serial (USB)

Example commands sent from GUI:

b"e": Open garage

b"g": Close garage

b"m": Open main door

b"d": Close main door

b"n": Request temperature data

