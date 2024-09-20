import serial
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from Door import s1
# Khởi tạo biến trạng thái
bedroom_light_status = False
door_status = False
background_images = {
    "Day": "daybr.jpg",
    "Night": "nightbr.jpg"
}
current_bg_key = "Day"  # Thiết lập hình nền ban đầu

def toggle_door():
    global door_status
    try:
        if door_status:
            s1.write(b'd')  # Close door
            door_status = False
        else:
            s1.write(b'm')  # Open door
            door_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def toggle_bedroom_light():
    global bedroom_light_status
    try:
        if bedroom_light_status:
            s1.write(b'0')  # Tắt đèn phòng ngủ
            bedroom_light_status = False
        else:
            s1.write(b'1')  # Bật đèn phòng ngủ
            bedroom_light_status = True
        # Cập nhật hình ảnh của nút đèn phòng ngủ
        light_button.config(image=light_on_img if bedroom_light_status else light_off_img)
        # Thay đổi hình nền dựa trên trạng thái đèn phòng ngủ
        if bedroom_light_status:
            change_background("Night")
        else:
            change_background("Day")
    except serial.SerialException as e:
        messagebox.showerror("Lỗi", f"Lỗi gửi lệnh đến Arduino: {e}")

def bedroom_light_blink():
    try:
        s1.write(b'2')  # Nhấp nháy đèn phòng ngủ
    except serial.SerialException as e:
        messagebox.showerror("Lỗi", f"Lỗi gửi lệnh đến Arduino: {e}")

def read_temperature():
    try:
        s1.write(b'n')  # Yêu cầu đọc nhiệt độ
        temperature_data = s1.readline().decode().strip()  # Đọc dữ liệu nhiệt độ từ Arduino
        temperature_label.config(text=f"Nhiệt độ: {temperature_data} °C")
        root.after(1000, read_temperature)
    except serial.SerialException as e:
        messagebox.showerror("Lỗi", f"Lỗi gửi yêu cầu đến Arduino: {e}")

def change_background(option):
    global current_bg_key
    current_bg_key = option
    image_path = background_images[option]
    load_new_background(image_path)

def back():
    root.destroy()
    os.system("python Host.py")

def load_new_background(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600))  # Đổi kích thước để phù hợp kích thước cửa sổ
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.configure(image=background_photo)
    background_label.image = background_photo  # Giữ tham chiếu
    root.configure(bg="#F0F0F0")  # Đặt lại màu nền nếu cần thiết

# Thiết lập cửa sổ tkinter
root = Tk()
root.title("BedRoom")
root.geometry("800x600+100+100")  # Thiết lập kích thước cửa sổ
root.configure(bg="#F0F0F0")

# Tải hình nền ban đầu
background_image_path = background_images[current_bg_key]
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600))  # Đổi kích thước để phù hợp cửa sổ
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Label để hiển thị nhiệt độ
temperature_label = Label(root, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label.place(x=530, y=100)

# Hàm để thay đổi kích thước ảnh
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

# Tải và thay đổi kích thước các hình ảnh cho các nút
door_img = resize_image("door.jpg", 150, 80)
light_on_img = resize_image("light_on.jpg", 150, 80)
light_off_img = resize_image("light_off.jpg", 150, 80)
blink_img = resize_image("blink.jpg", 150, 80)
back_img = resize_image("back.jpg", 150, 80)

# Tạo các nút với hình ảnh
door_button = Button(root, image=door_img, command=toggle_door, bd=0)
door_button.place(x=50, y=50)

# Ban đầu nút light sẽ có hình ảnh tùy thuộc vào trạng thái ban đầu của bedroom_light_status
light_button = Button(root, image=light_on_img if bedroom_light_status else light_off_img, command=toggle_bedroom_light, bd=0)
light_button.place(x=50, y=140)

blink_button = Button(root, image=blink_img, command=bedroom_light_blink, bd=0)
blink_button.place(x=50, y=230)

back_button = Button(root, image=back_img, command=back, bd=0)
back_button.place(x=620, y=500)

# Bắt đầu cập nhật nhiệt độ ngay lập tức
root.after(1000, read_temperature)

root.mainloop()
