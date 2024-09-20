import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import cv2
import time
import os
import serial

livingroom_light_status = False
fan_status = False
door_status = False

# Global variables
wrong_attempts = 0
unlocked_video_path = 'wc.mp4'  # Path to your video file
error_image_path = 'Lock.jpg'  # Path to your error image file
door_status = False  # Door status for smart home control panel
bedroom_light_status = False
livingroom_light_status = False
background_images = {
    "Day": "daybr.jpg",
    "Night": "nightbr.jpg",
}
background_images_lvr = {
    "DayLivingroom": "daylvr.jpg",
    "NightLivingroom": "nightlvr.jpg"
}
current_bg_key = "Day"  # Initial background
current_bg_livingroom_key = "DayLivingroom"  # Initial living room background

# Khởi tạo kết nối serial
try:
    s1 = serial.Serial('COM7', 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")

# Function to check password and handle login
def check_password():
    global wrong_attempts
    password = entry.get()
    if password == '1111':  # Replace with your actual password
        print("Đăng nhập thành công!")
        show_frame(video_frame)  # Switch to video frame
        play_unlocked_video(unlocked_video_path)  # Play the video
    else:
        wrong_attempts += 1
        if wrong_attempts >= 3:
            both_lights_blink()
            show_error_image()
        else:
            messagebox.showerror("Lỗi", "Sai mật khẩu! Bạn còn {} lần thử.".format(3 - wrong_attempts))
            entry.delete(0, tk.END)

# Function to play unlocked video using OpenCV
def play_unlocked_video(unlocked_video_path):
    cap = cv2.VideoCapture(unlocked_video_path)
    start_time = time.time()

    def update_frame():
        nonlocal start_time
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            show_frame(control_panel_frame)  # Switch to control panel frame
            return

        # Resize frame to fit the desired dimensions (e.g., 800x600)
        resized_frame = cv2.resize(frame, (800, 600))

        cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Check if 2.3 seconds have passed since the video started
        if time.time() - start_time >= 2.3:
            cap.release()
            cv2.destroyAllWindows()
            show_frame(control_panel_frame)  # Switch to control panel frame
            return

        video_label.after(15, update_frame)

    update_frame()

# Function to show error image
def show_error_image():
    error_window = tk.Toplevel()
    error_window.geometry('800x600+100+100')

    error_image = Image.open(error_image_path)
    error_image = error_image.resize((800, 600), Image.Resampling.LANCZOS)
    error_photo = ImageTk.PhotoImage(error_image)

    error_label = tk.Label(error_window, image=error_photo)
    error_label.image = error_photo  # Keep a reference
    error_label.pack()

    def close_error_window():
        error_window.destroy()

    error_window.after(5000, close_error_window)  # Close after 5 seconds

def both_lights_blink():
    try:
        s1.write(b"6")
    except Exception as e:
        print(f"Error: {e}")

# Function to show specified frame
def show_frame(frame):
    frame.tkraise()

# Function to toggle door status in control panel
def toggle_door():
    global door_status
    try:
        if door_status:
            s1.write(b"d")  # Đóng cửa
            door_status = False
        else:
            s1.write(b"m")  # Mở cửa
            door_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def living_room():
    show_frame(living_room_frame)

def bedroom():
    show_frame(bedroom_frame)

def garage():
    os.system("python garage.py")

def toggle_bedroom_light():
    global bedroom_light_status
    try:
        if bedroom_light_status:
            s1.write(b'0')  # Turn off bedroom light
            bedroom_light_status = False
            change_background("Day")  # Change to day background
        else:
            s1.write(b'1')  # Turn on bedroom light
            bedroom_light_status = True
            change_background("Night")  # Change to night background
        # Update light button image
        light_button.config(image=light_on_img if bedroom_light_status else light_off_img)
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending command to Arduino: {e}")

def bedroom_light_blink():
    try:
        s1.write(b'2')  # Blink bedroom light
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending command to Arduino: {e}")

def read_temperature():
    try:
        s1.write(b'n')  # Request temperature reading
        temperature_data = s1.readline().decode().strip()  # Read temperature data from Arduino
        temperature_label.config(text=f"Nhiệt độ phòng ngủ: {temperature_data} °C")
        temperature_label_livingroom.config(text=f"Nhiệt độ phòng khách: {temperature_data} °C")
        W.after(1000, read_temperature)  # Update every second
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending request to Arduino: {e}")

def toggle_livingroom_light():
    global livingroom_light_status
    try:
        if livingroom_light_status:
            s1.write(b"4")  # Turn off living room light
            livingroom_light_status = False
            change_background_livingroom("DayLivingroom")  # Change to day background
        else:
            s1.write(b"3")  # Turn on living room light
            livingroom_light_status = True
            change_background_livingroom("NightLivingroom")  # Change to night background
        light_button_livingroom.config(image=light_on_img if livingroom_light_status else light_off_img)
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def livingroom_light_blink():
    try:
        s1.write(b"5")  # Blink living room light
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def toggle_fan():
    global fan_status
    try:
        if fan_status:
            s1.write(b"t")  # Turn off fan
            fan_status = False
        else:
            s1.write(b"b")  # Turn on fan
            fan_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def change_background_livingroom(option):
    global current_bg_livingroom_key
    current_bg_livingroom_key = option
    image_path = background_images_lvr[option]
    load_new_background_livingroom(image_path)

def load_new_background_livingroom(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
    background_photo = ImageTk.PhotoImage(background_image)
    background_label_livingroom.config(image=background_photo)
    background_label_livingroom.image = background_photo  # Keep a reference

def change_background(option):
    global current_bg_key
    current_bg_key = option
    image_path = background_images[option]
    load_new_background(image_path)

def load_new_background(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.image = background_photo  # Keep a reference

def back_to_main():
    show_frame(control_panel_frame)

# Main Tkinter window
W = tk.Tk()
W.geometry('800x600+100+100')

# Create frames
password_frame = tk.Frame(W)
video_frame = tk.Frame(W)
control_panel_frame = tk.Frame(W)
bedroom_frame = tk.Frame(W)
living_room_frame = tk.Frame(W)

for frame in (password_frame, video_frame, control_panel_frame, bedroom_frame, living_room_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Password frame
A = Image.open('Bill.png')  # Replace with your image path
A = A.resize((800, 600), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(A)

L1 = tk.Label(password_frame, image=photo)
L1.image = photo  # Keep a reference
L1.pack(pady=20)

custom_font = tkfont.Font(family="Algerian", size=20)

label_password = tk.Label(password_frame, text="Nhập mật khẩu:", bg="black", fg="white", font=custom_font)
label_password.place(x=50, y=280)

entry = tk.Entry(password_frame, show="*", bg="black", fg="white", font=custom_font, width=10)
entry.place(x=70, y=330)

entry.bind("<Return>", lambda event: check_password())
entry.bind("<KeyRelease>", lambda event: on_key_release(event))

def on_key_release(event):
    if len(entry.get()) == 4:
        check_password()

# Video frame
video_label = tk.Label(video_frame)
video_label.pack()

# Control panel frame
control_panel_frame.configure(bg="#F0F0F0")

# Background image for control panel frame
background_image_path = "H.jpg"
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(control_panel_frame, image=background_photo)
background_label.image = background_photo  # Keep a reference
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def create_button_image(path, size):
    button_image = Image.open(path)
    button_image = button_image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(button_image)

# Door button
button_image_path = "Door.jpg"
button_photo = create_button_image(button_image_path, (200, 100))

door_button = tk.Button(control_panel_frame, image=button_photo, command=toggle_door, relief=tk.RIDGE)
door_button.image = button_photo  # Keep a reference
door_button.place(x=10, y=485)

# Living room button
living_room_image_path = "LivingRoom.jpg"
living_room_photo = create_button_image(living_room_image_path, (200, 100))

living_room_button = tk.Button(control_panel_frame, image=living_room_photo, command=living_room, relief=tk.RIDGE)
living_room_button.image = living_room_photo  # Keep a reference
living_room_button.place(x=10, y=10)

# Bedroom button
bedroom_image_path = "Bedroom.jpg"
bedroom_photo = create_button_image(bedroom_image_path, (200, 100))

bedroom_button = tk.Button(control_panel_frame, image=bedroom_photo, command=bedroom, relief=tk.RIDGE)
bedroom_button.image = bedroom_photo  # Keep a reference
bedroom_button.place(x=10, y=120)

# Garage button
garage_image_path = "GARAGE.jpg"
garage_photo = create_button_image(garage_image_path, (200, 100))

garage_button = tk.Button(control_panel_frame, image=garage_photo, command=garage, relief=tk.RIDGE)
garage_button.image = garage_photo  # Keep a reference
garage_button.place(x=10, y=230)

# Bedroom frame
# Load initial background
background_image_path = background_images[current_bg_key]
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
background_photo = ImageTk.PhotoImage(background_image)

background_label_bedroom = tk.Label(bedroom_frame, image=background_photo)
background_label_bedroom.place(x=0, y=0, relwidth=1, relheight=1)

# Bedroom frame
temperature_label = tk.Label(bedroom_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label.place(x=530, y=100)

# Living room frame
background_image_path_livingroom = background_images_lvr[current_bg_livingroom_key]
background_image_livingroom = Image.open(background_image_path_livingroom)
background_image_livingroom = background_image_livingroom.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
background_photo_livingroom = ImageTk.PhotoImage(background_image_livingroom)

background_label_livingroom = tk.Label(living_room_frame, image=background_photo_livingroom)
background_label_livingroom.place(x=0, y=0, relwidth=1, relheight=1)

temperature_label_livingroom = tk.Label(living_room_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label_livingroom.place(x=140, y=150)

# Function to resize image
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

# Load and resize button images
door_img = resize_image("door.jpg", 150, 80)
light_on_img = resize_image("light_on.jpg", 150, 80)
light_off_img = resize_image("light_off.jpg", 150, 80)
blink_img = resize_image("blink.jpg", 150, 80)
back_img = resize_image("back.jpg", 150, 80)
fan_img = resize_image("fan.jpg", 150, 80)
return_img = resize_image("back.jpg", 150, 80)

# Create buttons with images for bedroom frame
door_button_bedroom = tk.Button(bedroom_frame, image=door_img, command=toggle_door, bd=0)
door_button_bedroom.place(x=50, y=50)

light_button = tk.Button(bedroom_frame, image=light_on_img if bedroom_light_status else light_off_img, command=toggle_bedroom_light, bd=0)
light_button.place(x=50, y=140)

blink_button = tk.Button(bedroom_frame, image=blink_img, command=bedroom_light_blink, bd=0)
blink_button.place(x=50, y=230)

back_button = tk.Button(bedroom_frame, image=back_img, command=back_to_main, bd=0)
back_button.place(x=620, y=500)

# Create buttons with images for living room frame
light_button_livingroom = tk.Button(living_room_frame, image=light_on_img if livingroom_light_status else light_off_img, command=toggle_livingroom_light, bd=0)
light_button_livingroom.place(x=600, y=50)

btn_livingroom_blink = tk.Button(living_room_frame, image=blink_img, command=livingroom_light_blink, bd=0)
btn_livingroom_blink.place(x=600, y=140)

btn_toggle_fan = tk.Button(living_room_frame, image=fan_img, command=toggle_fan, bd=0)
btn_toggle_fan.place(x=600, y=230)

btn_door = tk.Button(living_room_frame, image=door_img, command=toggle_door, bd=0)
btn_door.place(x=600, y=320)

btn_return = tk.Button(living_room_frame, image=return_img, command=back_to_main, bd=0)
btn_return.place(x=600, y=500)

# Start updating temperature
W.after(1000, read_temperature)

# Show the password frame initially
show_frame(password_frame)

# Close serial connection on exit
def close_serial():
    if s1.is_open:
        s1.close()

def on_closing():
    close_serial()
    W.destroy()

W.protocol("WM_DELETE_WINDOW", on_closing)

W.mainloop()
