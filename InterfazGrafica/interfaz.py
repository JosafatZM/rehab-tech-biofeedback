import customtkinter as ctk
import threading
import os
from PIL import Image
from MediaPipe.modelo import modelo

class FuncionesPrograma:

    def ventanas_respaldo(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Consulta")

objeto_funciones = FuncionesPrograma()

class NavigationFrame(ctk.CTkFrame):

    def __init__(self, master, corner_radius, title, logo, home_button_image, database_button_image, home_button_command, database_button_command):
        super().__init__(master)

        self.corner_radius = corner_radius
        self.title = title
        self.logo = logo
        self.home_button_image = home_button_image
        self.database_button_image = database_button_image
        self.home_button_command = home_button_command
        self.database_button_command = database_button_command
        
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(4, weight=1)

        # logo and title
        self.title = ctk.CTkLabel(self, text= self.title, compound='left', image=self.logo,
                                            font= ctk.CTkFont(size=15, weight='bold'))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Home button
        self.home_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_button_image, anchor="w", command=self.home_button_command )
        self.home_button.grid(row=1, column=0, sticky="ew")

        # Data base button
        self.data_base_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Data Base",
                                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       image=self.database_button_image, anchor="w", command=self.database_button_command)
        self.data_base_button.grid(row=2, column=0, sticky="ew")

        # dark or light mode switch menu 
        self.appearance_mode_menu = ctk.CTkOptionMenu(self, values=["Dark", "Light",  "System"],
                                                                command=self.change_appearance_mode_event,
                                                                fg_color="#081016",
                                                                button_color="#00090b",
                                                                button_hover_color="#000000")
        
        self.appearance_mode_menu.grid(row=6, column=0, padx=10, pady=250, sticky="s")

    # dark or light mode switch thing
    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

class HomeFrame(ctk.CTkFrame):

    def __init__(self, master, corner_radius, fg_color, logo):
        super().__init__(master)

        self.corner_radius = corner_radius
        self.fg_color = fg_color
        self.logo = logo
        self.grid_columnconfigure(0, weight=1)

        self.logo_image = ctk.CTkLabel(self, text="", image=self.logo)
        self.logo_image.grid(row=0, column=0, padx=20, pady=10)

        self.model_button = ctk.CTkButton(self, text="Model", command=self.video, hover_color="#00090b", fg_color="#081016")
        self.model_button.grid(row=1, column=0, padx=20, pady=10)

    # creates the video thread object
    def video(self):
        
        video_thread_instance = threading.Thread(target= modelo)
        video_thread_instance.start()

class DataBaseFrame(ctk.CTkFrame):

    def __init__(self, master, corner_radius, fg_color, logo):
        super().__init__(master)

        self.corner_radius = corner_radius
        self.fg_color = fg_color
        self.logo = logo
        self.grid_columnconfigure(0, weight=1)

        self.logo_image = ctk.CTkLabel(self, text="", image=self.logo)
        self.logo_image.grid(row=0, column=0, padx=20, pady=10)

        self.button = ctk.CTkButton(self, text="Consultar", command= objeto_funciones.ventanas_respaldo, hover_color="#00090b", fg_color="#081016")
        self.button.grid(row=1, column=0, padx=20, pady=10)
        self.button = ctk.CTkButton(self, text="Exportar", command= objeto_funciones.ventanas_respaldo, hover_color="#00090b", fg_color="#081016")
        self.button.grid(row=2, column=0, padx=20, pady=10)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window title
        self.title('')
        # window size
        self.geometry("700x450")
        self.resizable(False, False)

        # set grid layout 1x2
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "logo_modular.png")), size=(40, 40))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "imagen8.png")), size=(500, 150))
        self.large_test_image2 = ctk.CTkImage(Image.open(os.path.join(image_path, "banner_base_datos.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        

        # Navigation Frame
        self.navigation_frame = NavigationFrame(self, corner_radius=0, title=' BioFeedback', logo=self.logo_image,
                                                home_button_image=self.home_image,
                                                database_button_image=self.add_user_image,
                                                home_button_command= self.home_button_event,
                                                database_button_command=self.database_button_event)
        
        # Home frame
        self.home_frame = HomeFrame(self, corner_radius=0, fg_color="transparent", logo=self.large_test_image)

        # Data base frame
        self.data_base_frame = DataBaseFrame(self, corner_radius=0, fg_color="transparent", logo= self.large_test_image2)

        # select default frame
        self.select_frame_by_name("home")
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.navigation_frame.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.navigation_frame.data_base_button.configure(fg_color=("gray75", "gray25") if name == "database" else "transparent")
        
        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.home_frame.configure(fg_color="transparent")
        else:
            self.home_frame.grid_forget()
        if name == "database":
            self.data_base_frame.grid(row=0, column=1, sticky="nsew")
            self.data_base_frame.configure(fg_color="transparent")
            
        else:
            self.data_base_frame.grid_forget()
    

    def home_button_event(self):
        self.select_frame_by_name("home")

    def database_button_event(self):
        self.select_frame_by_name("database")


app = App()
app.mainloop()