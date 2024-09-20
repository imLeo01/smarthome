import serial
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame

# Initialize pygame mixer
pygame.mixer.init()

root = Tk()
root.title("Living Room")
root.geometry("800x600+100+100")
root.configure(bg="#F0F0F0")

background_image_path = "garage1.jpg"
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600))
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

door_status = False
door_garage = False

songs = {
    "Song 1": "opn.mp3",
    "Song 2": "opn.mp3",
    "Song 3": "opn.mp3"
}

current_song = "opn.mp3"  # Set the default current song

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

def return_to_main():
    root.destroy()
    os.system("python Host.py")

def garage_door():
    global door_garage
    try:
        if door_garage:
            s1.write(b"g")  # Close door
            door_garage = False
        else:
            s1.write(b"e")  # Open door
            door_garage = True
        # Update the button image
        btn_door_garage.config(image=down_img if door_garage else up_img)
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

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

def update_temperature():
    try:
        s1.write(b"n")  # Request temperature reading
        temperature_data = s1.readline().decode().strip()  # Read temperature data from Arduino
        temperature_label.config(text=f"Temperature: {temperature_data} °C")
        # Schedule the next update in 1 second (1000 ms)
        root.after(1000, update_temperature)
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def play_song():
    global current_song
    selected_song = song_var.get()
    if selected_song != current_song:
        current_song = selected_song
        song_path = songs[selected_song]
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=-1)  # loops=-1 to loop indefinitely

door_img = resize_image("door.jpg", 150, 80)
up_img = resize_image("up.jpg", 150, 80)
down_img = resize_image("down.jpg", 150, 80)
return_img = resize_image("back.jpg", 150, 80)

btn_door_garage = Button(root, image=(down_img if door_garage else up_img), command=garage_door, bd=0)
btn_door_garage.place(x=600, y=30)

# Frame to hold the Radiobuttons
radio_frame = Frame(root, bg="#F0F0F0")
radio_frame.place(x=600, y=120)

song_var = StringVar(value=current_song)

for song_name in songs.keys():
    radio = Radiobutton(radio_frame, text=song_name, variable=song_var, value=song_name, command=play_song, bg="#F0F0F0")
    radio.pack(anchor=W)

btn_door = Button(root, image=door_img, command=toggle_door, bd=0)
btn_door.place(x=600, y=240)

btn_return = Button(root, image=return_img, command=return_to_main, bd=0)
btn_return.place(x=600, y=500)

temperature_label = Label(root, text="Temperature: --", font="Helvetica 12 bold", bg='white')
temperature_label.place(x=280, y=190)

# Play the default song when the application starts
play_song()

root.mainloop()
