import customtkinter as ctk
from tkinter.font import BOLD
from DataBase.data_base import BaseDatos as bd
from DataBase.data_base import acceso_bd

# para manipular la base de datos
base_datos = bd(**acceso_bd)

widgets_font = ('Relaway', 16, BOLD)

entry_width = 400 - 2 * (10 + 10 + 80)  


class RegistFrame(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title('')
        self.geometry("300x330")
        self.grab_set()
        self.resizable(False, False)

        # Create text
        self.texto_nombre = ctk.CTkTextbox(self, width=90, corner_radius=5, height= 30)
        self.texto_nombre.grid(row=1, column=1, padx=20, pady=5, sticky="ew")
        self.texto_nombre.insert("0.0", "Nombre:" )

        self.texto_apellido = ctk.CTkTextbox(self, width=90, corner_radius=5,height= 30)
        self.texto_apellido.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        self.texto_apellido.insert("0.0", "Apellido:" )

        self.texto_sexo = ctk.CTkTextbox(self, width=90, corner_radius=5,height= 30)
        self.texto_sexo.grid(row=3, column=1, padx=20, pady=5, sticky="ew")
        self.texto_sexo.insert("0.0", "Sexo:" )

        self.texto_edad= ctk.CTkTextbox(self, width=90, corner_radius=5,height= 30)
        self.texto_edad.grid(row=4, column=1, padx=20, pady=5, sticky="ew")
        self.texto_edad.insert("0.0", "Edad:" )

        self.texto_lateralidad = ctk.CTkTextbox(self, width=90, corner_radius=5,height= 30,activate_scrollbars=False)
        self.texto_lateralidad.grid(row=5, column=1, padx=20, pady=5, sticky="ew")
        self.texto_lateralidad.insert("0.0", "Lateralidad:" )
        
        # Create entries
        self.entrada_nombre = ctk.CTkEntry(self, corner_radius=5, height= 30)
        self.entrada_nombre.configure(font= widgets_font)
        self.entrada_nombre.grid(row=1, column=2, padx=10, pady=10, sticky= 'ew')

        self.entrada_apellido = ctk.CTkEntry(self, corner_radius=5, height= 30)
        self.entrada_apellido.configure(font= widgets_font)
        self.entrada_apellido.grid(row=2, column=2, padx=10, pady=10, sticky= 'ew')

        self.entrada_sexo = ctk.CTkEntry(self, corner_radius=5, height= 30)
        self.entrada_sexo.configure(font= widgets_font)
        self.entrada_sexo.grid(row=3, column=2, padx=10, pady=10, sticky= 'ew')

        self.entrada_edad = ctk.CTkEntry(self, corner_radius=5, height= 30)
        self.entrada_edad.configure(font= widgets_font)
        self.entrada_edad.grid(row=4, column=2, padx=10, pady=10, sticky= 'ew')

        self.entrada_lateralidad = ctk.CTkEntry(self, corner_radius=5, height= 30)
        self.entrada_lateralidad.configure(font= widgets_font)
        self.entrada_lateralidad.grid(row=5, column=2, padx=10, pady=10, sticky= 'ew')

        # Register Button
        self.boton_registrar = ctk.CTkButton(self, text="Registrar", 
                                          command= self.registrar,
                                          width=200,
                                          anchor="center",
                                          hover_color="#00090b",
                                          fg_color="#081016")
        self.boton_registrar.grid(row=0, column=1, columnspan=2,padx=10, pady=10)


    def registrar(self):
        try:
            nombre = self.entrada_nombre.get().title()
            apellido = self.entrada_apellido.get().title()
            sexo = self.entrada_sexo.get().title()
            edad = int(self.entrada_edad.get())
            lateralidad = self.entrada_lateralidad.get().title()
            
            print(f"Datos Registrados \n"
                  f"Nombre: {nombre}\n"
                  f"Apellido: {apellido}\n"
                  f"Sexo: {sexo}\n"
                  f"Edad: {edad}, DataType: {type(edad)}\n"
                  f"Lateralidad: {lateralidad}\n")
        
        except:
            pass
        