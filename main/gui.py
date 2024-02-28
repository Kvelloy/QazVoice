import customtkinter
import os
from PIL import Image
import webbrowser

 
class App(customtkinter.CTk):

    str_text = ""

    def __init__(self):

        super().__init__()

        self.title("QazVoice")

        self.geometry("700x410")

 

        # set grid layout 1x2

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)

 

        # load images with light and dark mode image

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")

        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(50, 50))

           

        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large.png")), size=(700, 180))

           

        self.micro_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "micro_light.png")), size=(70, 70))

           

        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))

 

        self.info_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "info.png")), size=(70, 70))

 

        self.setting_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "settings.png")), size=(70, 70))

 

        # create navigation frame

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        self.navigation_frame.grid_rowconfigure(4, weight=1)

 

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  QazVoice", image=self.logo_image,

                                                            compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))

        self.navigation_frame_label.grid(row=0, column=0, padx=60, pady=60)

 

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",

                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),

                                                    image=self.home_image, anchor="w", command=self.home_button_event)

        self.home_button.grid(row=1, column=0, sticky="ew")

 

 

 

        # create home frame

        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.home_frame.grid_columnconfigure(0, weight=1)

 

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="QazVoice Assistant", font=("Montserrat" , 20), image=self.large_test_image)

        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

 

 

        self.home_button_2 = customtkinter.CTkButton(self.home_frame,text="" , image=self.info_image, command=self.info_event)

        self.home_button_2.grid(row=1, column=0, padx=20, pady=10)

 

        self.home_button_3 = customtkinter.CTkButton(self.home_frame, text="", image=self.setting_image , command=self.settings_event)

        self.home_button_3.grid(row=2, column=0, padx=20, pady=10)

           

 

        self.select_frame_by_name("home")

 

    def select_frame_by_name(self, name):

        # set button color for selected button

        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        if name == "home":

            self.home_frame.grid(row=0, column=1, sticky="nsew")

        else:

            self.home_frame.grid_forget()

           

 

    def home_button_event(self):

        self.select_frame_by_name("home")

 

    def info_event(self):

        webbrowser.open("https://www.canva.com/design/DAFwQ0b2BCc/j6HHe1nLrOIDpcTp7Cdw7A/edit" , new=2)

 

    def settings_event(self):

        os.system("config.py")

    def change_appearance_mode_event(self, new_appearance_mode):

        customtkinter.set_appearance_mode(new_appearance_mode)

 

 



