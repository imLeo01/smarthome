import serial
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Giả lập đối tượng serial


livingroom_light_status = False
fan_status = False
door_status = False

# Biến toàn cục để giữ hình ảnh nút đèn
light_on_img = None
light_off_img = None

def toggle_door():
    global door_status
    try:
        if door_status:
            s1.write(b"d")  # Close door
            door_status = False
        else:
            s1.write(b"m")  # Open door
            door_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def toggle_livingroom_light():
    global livingroom_light_status, light_button
    try:
        if livingroom_light_status:
            s1.write(b"4")  # Turn off living room light
            livingroom_light_status = False
            change_background("daylvr.jpg")
            light_button.config(image=light_off_img)  # Cập nhật hình ảnh nút
        else:
            s1.write(b"3")  # Turn on living room light
            livingroom_light_status = True
            change_background("nightlvr.jpg")
            light_button.config(image=light_on_img)  # Cập nhật hình ảnh nút
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

def update_temperature():
    try:
        s1.write(b"n")  # Request temperature reading
        temperature_data = s1.readline().decode().strip()  # Read temperature data from Arduino
        temperature_label.config(text=f"Temperature: {temperature_data} °C")
        # Schedule the next update in 1 second (1000 ms)
        root.after(1000, update_temperature)
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")


def change_background(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600))
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.configure(image=background_photo)
    background_label.image = background_photo

def return_to_main():
    root.destroy()
    os.system("python Host.py")

# Hàm để thay đổi kích thước ảnh
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

root = Tk()
root.title("Living Room")
root.geometry("800x600+100+100")
root.configure(bg="#F0F0F0")

background_image_path = "daylvr.jpg"
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600))
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Tải và thay đổi kích thước các hình ảnh cho các nút
door_img = resize_image("Door.jpg", 150, 80)
light_on_img = resize_image("light_on.jpg", 150, 80)
light_off_img = resize_image("light_off.jpg", 150, 80)
blink_img = resize_image("blink.jpg", 150, 80)
fan_img = resize_image("fan.jpg", 150, 80)
return_img = resize_image("back.jpg", 150, 80)

# Tạo các nút với hình ảnh
light_button = Button(root, image=(light_on_img if livingroom_light_status else light_off_img), command=toggle_livingroom_light, bd=0)
light_button.place(x=600, y=50)

btn_livingroom_blink = Button(root, image=blink_img, command=livingroom_light_blink, bd=0)
btn_livingroom_blink.place(x=600, y=140)

btn_toggle_fan = Button(root, image=fan_img, command=toggle_fan, bd=0)
btn_toggle_fan.place(x=600, y=230)

btn_door = Button(root, image=door_img, command=toggle_door, bd=0)
btn_door.place(x=600, y=320)

btn_return = Button(root, image=return_img, command=return_to_main, bd=0)
btn_return.place(x=600, y=500)

# Label to display temperature
temperature_label = Label(root, text="Temperature: --", font="Helvetica 12 bold", bg='white')
temperature_label.place(x=140, y=150)

# Start updating temperature immediately
root.after(1000, update_temperature)

root.mainloop()
