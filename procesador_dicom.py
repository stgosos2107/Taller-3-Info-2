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

    def __init__(self, carpeta):
        # Carpeta donde están los DICOM
        self.carpeta = carpeta
        self.datasets = []      # Aquí se guardan los DICOM leídos
        self.rutas_archivos = []  # Ruta de cada archivo leído
        self.df = pd.DataFrame()  # DataFrame final con metadatos

#Este método recorre la carpeta y trata de leer todos los DICOM
    def cargar_archivos(self):
        """Recorre la carpeta y trata de leer todos los DICOM."""
        if not os.path.isdir(self.carpeta):
            print("La ruta no es un directorio:", self.carpeta)
            return

        print("Buscando archivos en:", self.carpeta)

        for raiz, _, archivos in os.walk(self.carpeta):
            for nombre in archivos:
                ruta = os.path.join(raiz, nombre)
                try:
                    ds = pydicom.dcmread(ruta)
                    self.datasets.append(ds)
                    self.rutas_archivos.append(ruta)
                    print("DICOM leído:", ruta)
                except Exception:
                    # Si no es DICOM o hay error, simplemente lo ignoramos
                    print("Archivo ignorado (no DICOM o dañado):", ruta)

        print("Total de DICOM válidos:", len(self.datasets))
    
#Devuelve el atributo como string si existe, o None
    def _get_str(self, ds, nombre_attr):
        valor = getattr(ds, nombre_attr, None)
        if valor is None:
            return None
        return str(valor)

#Saca los metadatos principales de cada DICOM y arma el DataFrame
    def extraer_metadatos(self):
        
        if not self.datasets:
            print("Primero carga los archivos DICOM.")
            return

        filas = []
        for ruta, ds in zip(self.rutas_archivos, self.datasets):
            fila = {
                "RutaArchivo": ruta,
                "PatientID": self._get_str(ds, "PatientID"),
                "PatientName": self._get_str(ds, "PatientName"),
                "StudyInstanceUID": self._get_str(ds, "StudyInstanceUID"),
                "StudyDescription": self._get_str(ds, "StudyDescription"),
                "StudyDate": self._get_str(ds, "StudyDate"),
                "Modality": self._get_str(ds, "Modality"),
                "Rows": getattr(ds, "Rows", None),
                "Columns": getattr(ds, "Columns", None),
            }
            filas.append(fila)

        self.df = pd.DataFrame(filas)
        print("Metadatos cargados en DataFrame. Filas:", len(self.df))

#Calcula la intensidad promedio de los píxeles de cada imagen.
    def calcular_intensidad_promedio(self):
        if self.df.empty:
            print("Primero extrae los metadatos.")
            return

        intensidades = []
        for i, ds in enumerate(self.datasets):
            try:
                arr = ds.pixel_array.astype(np.float32)
                prom = float(arr.mean())
                intensidades.append(prom)
                print(f"Intensidad promedio [{i}]:", prom)
            except Exception:
                # Si no se puede leer la imagen, ponemos NaN
                intensidades.append(np.nan)
                print(f"No se pudo calcular intensidad para el índice {i}")

        self.df[self.COLUMNA_INTENSIDAD] = intensidades
        print("Columna de intensidad promedio agregada.")
    
#Guarda el DataFrame en un archivo CSV
    def guardar_csv(self, ruta_salida):
        if self.df.empty:
            print("No hay datos para guardar en CSV.")
            return

        self.df.to_csv(ruta_salida, index=False)
        print("CSV guardado en:", ruta_salida)


#Menu principal con cual interectua el usuario
def main():
    print("Procesador DICOM-Informática 2 ")
    carpeta = input("Ingresa la ruta absoluta del directorio con archivos DICOM: ").strip()

    if not carpeta:
        print("No escribiste la ruta. Saliendo.")
        return

    nombre_csv = input(
        "Indica el nombre del archivo CSV de salida "
        "(Enter para usar 'metadatos_dicom.csv'): "
    ).strip()

    if not nombre_csv:
        nombre_csv = "metadatos_dicom.csv"

    procesador = ProcesadorDICOM(carpeta)

    # 1. Cargar DICOM
    procesador.cargar_archivos()
    if not procesador.datasets:
        print("No se cargó ningún DICOM. Revisa la ruta.")
        return

    # 2. Metadatos
    procesador.extraer_metadatos()

    # 3. Intensidad promedio
    procesador.calcular_intensidad_promedio()

    # 4. Guardar CSV
    procesador.guardar_csv(nombre_csv)


if __name__ == "__main__":
    main()
