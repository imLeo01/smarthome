# Add new images for buttons corresponding to each background
button_images_control_panel = {
    "Song 1": {
        "hjhj": "sim.jpg",
        "sd": "shit.jpg",
        "door": "Door.jpg",
        "living_room": "LivingRoom.jpg",
        "bedroom": "Bedroom.jpg",
        "garage": "GARAGE.jpg"
    },
    "Song 2": {
        "hjhj": "new_sim.jpg",  # replace with actual image path
        "sd": "new_shit.jpg",  # replace with actual image path
        "door": "new_Door.jpg",  # replace with actual image path
        "living_room": "new_LivingRoom.jpg",  # replace with actual image path
        "bedroom": "new_Bedroom.jpg",  # replace with actual image path
        "garage": "new_GARAGE.jpg"  # replace with actual image path
    }
}

# Modify the load_new_background_control_panel function to update button images
def load_new_background_control_panel(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label_control_panel.config(image=background_photo)
    background_label_control_panel.image = background_photo  # Keep a reference

    # Update button images
    update_button_images_control_panel(current_bg_key)

def update_button_images_control_panel(bg_key):
    hjhj_button.config(image=create_button_image(button_images_control_panel[bg_key]["hjhj"], (200, 100)))
    sd_button.config(image=create_button_image(button_images_control_panel[bg_key]["sd"], (200, 100)))
    door_button.config(image=create_button_image(button_images_control_panel[bg_key]["door"], (200, 100)))
    living_room_button.config(image=create_button_image(button_images_control_panel[bg_key]["living_room"], (200, 100)))
    bedroom_button.config(image=create_button_image(button_images_control_panel[bg_key]["bedroom"], (200, 100)))
    garage_button.config(image=create_button_image(button_images_control_panel[bg_key]["garage"], (200, 100)))

# Function to create button images
def create_button_image(path, size):
    button_image = Image.open(path)
    button_image = button_image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(button_image)

# Initial setup of the control panel
initial_bg_path_control_panel = background_images_control_panel["Song 1"]
background_image_control_panel = Image.open(initial_bg_path_control_panel)
background_image_control_panel = background_image_control_panel.resize((800, 600), Image.Resampling.LANCZOS)
background_photo_control_panel = ImageTk.PhotoImage(background_image_control_panel)
background_label_control_panel = tk.Label(control_panel_frame, image=background_photo_control_panel)
background_label_control_panel.image = background_photo_control_panel

background_label_control_panel.place(x=0, y=0, relwidth=1, relheight=1)
background_label_control_panel.lower()

# Set initial button images
update_button_images_control_panel("Song 1")