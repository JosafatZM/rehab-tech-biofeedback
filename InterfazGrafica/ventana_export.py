import customtkinter as ctk
from tkinter.font import BOLD
from DataBase.data_base import BaseDatos as bd
from DataBase.data_base import acceso_bd
from tkinter.messagebox import *
import json

# para manipular la base de datos
base_datos = bd(**acceso_bd)

widgets_font = ('Relaway', 16, BOLD)

entry_width = 400 - 2 * (10 + 10 + 80)  

class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = ctk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = ctk.CTkButton(self, text="Exportar JSON", width=100, height=24,  hover_color="#00090b", fg_color="#081016")
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), padx=5, sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(10, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
            

class ExportFrame(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Exportar Datos")
        self.geometry("400x330")
        self.grab_set()
        self.resizable(False, False)

        # Ajuste del Entry
        # Ancho de la ventana - (2*padding) - (2*ancho de botones)
        self.columnconfigure(1, weight=1)
        self.entrada_de_busqueda = ctk.CTkEntry(self, width=entry_width)
        
        self.entrada_de_busqueda.configure(font= widgets_font)
        
        self.entrada_de_busqueda.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.boton_buscar = ctk.CTkButton(self, text="Buscar", 
                                          command= self.buscar,
                                          width=200,
                                          anchor="center",
                                          hover_color="#00090b",
                                          fg_color="#081016")
        
        self.boton_buscar.grid(row=0, column=1, padx=0.1, pady=10)

        
        # Se crea una etiqueta para mostrar el número de resultados
        self.resultados_label = ctk.CTkLabel(self,
                                            text="Esperando una instruccion...")
        self.resultados_label.grid(pady=10)   
        self.resultados_label.grid(row= 2, column= 0, columnspan= 3, padx= 10, pady= 10)              


    def label_button_frame_event(self, item):
        
            print(f"Exportando JSON: {item}")
            
            item = item.split(' ')
            query0 = f"SELECT id_sujeto FROM data_modular.participantes WHERE nombre = '{item[-2]}'"
            self.id = base_datos.consulta(query0)
            query = f"SELECT emg FROM data_modular.datos_emg WHERE id_sujeto = {self.id[0][0]}"
            query2 = f"SELECT angulos_codo FROM data_modular.datos_angulos WHERE id_sujeto = {self.id[0][0]}"
            query3 = f"SELECT angulos_hombro FROM data_modular.datos_angulos WHERE id_sujeto = {self.id[0][0]}"
            self.emg = base_datos.consulta(query)
            self.valores_angulares= base_datos.consulta(query2)
            self.valores_angulares_hombro = base_datos.consulta(query3)
       
            # tuple to list 
            self.emg = self.emg[0][0]
            self.emg = self.emg[1:-1].split(",")
            self.emg = [float(x) for x in self.emg]

            self.valores_angulares = self.valores_angulares[0][0]
            self.valores_angulares = self.valores_angulares.strip('{}')
            self.valores_angulares = self.valores_angulares.split(",")
            self.valores_angulares = {key[1:-2]: float(value) for key, value in (pair.split(': ') for pair in self.valores_angulares)}
            
            self.valores_angulares_hombro = self.valores_angulares_hombro[0][0]
            self.valores_angulares_hombro = self.valores_angulares_hombro.strip('{}')
            self.valores_angulares_hombro = self.valores_angulares_hombro.split(",")
            self.valores_angulares_hombro = {key[1:-2]: float(value) for key, value in (pair.split(': ') for pair in self.valores_angulares_hombro)}

            data = {
                "emg": self.emg, 
                "valores_angulares_codo": self.valores_angulares,
                "valores_angulares_hombro": self.valores_angulares_hombro
            }

            path =rf'C:\Users\Josaf\OneDrive - Universidad de Guadalajara\Proyecto_Modular\JSON\data_sujeto_id{self.id[0][0]}.json'

            
            # Guardar en un archivo .json
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)  # Usar indent=4 para hacerlo más legible

            showinfo('Exportación', 'Archivo JSON listo!')
           
            
        

    def buscar(self): 
            try:
                
                busqueda = self.entrada_de_busqueda.get().title() 

                query = f"SELECT nombre, apellido FROM data_modular.participantes WHERE nombre = '{busqueda}'"

                self.resultado = base_datos.consulta(query)

                if len(self.resultado):
                    # create scrollable label and button frame
                    self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self,
                                                                                    command=self.label_button_frame_event, 
                                                                                    corner_radius=0,
                                                                                    )
                    
                    self.scrollable_label_button_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

                    for nombre, apellido in self.resultado:  # Iterar sobre los elementos de la lista
                        self.scrollable_label_button_frame.add_item(f"Datos: {nombre} {apellido}")

                self.resultados_label.configure(text= f"Se encontraron {len(self.resultado)} resultado/s")
            except:
                pass