#Taller Informática 2 Unidad 3

#Creación de programa para leer DICOM, sacar metadatos y calcular la intensidad 
# promedio de cada imagen.


#Importaciones necesarias
import os
import numpy as np
import pandas as pd
import pydicom

class ProcesadorDICOM:
    COLUMNA_INTENSIDAD = "IntensidadPromdio"  # Se deja igual que en el enunciado del taller

    def _init_(self, carpeta):
        # Carpeta donde están los DICOM
        self.carpeta = carpeta
        self.datasets = []      # Aquí se guardan los DICOM leídos
        self.rutas_archivos = []  # Ruta de cada archivo leído
        self.df = pd.DataFrame()  # DataFrame final con metadatos

#Este método recorre la carpeta y trata de leer todos los DICOM
    def cargar_archivos(self):
        if not os.path.isdir(self.carpeta):
            print("La ruta no es un directorio:", self.carpeta)
            return
        
