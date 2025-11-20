# Taller Evaluativo – Informática 2: Unidad 3  
## Introducción a la informática médica

### Datos del curso

- **Asignatura:** Informática 2 – Unidad 3  
- **Tema:** Introducción a la informática médica y estándares DICOM/HL7  

### Integrantes del equipo

- **Estudiante 1:** Santiago Osorio Salazar  
- **Estudiante 2:** Sofia Henao Osorio  



# 1: Breve descripción del proyecto
 
El proyecto consiste en desarrollar un programa en Python capaz de leer automáticamente un conjunto de archivos médicos en formato **DICOM**, extraer sus metadatos más importantes y realizar un análisis sencillo sobre las imágenes.  

El flujo general es:

1. El usuario indica la **ruta de un directorio** donde se encuentran los archivos DICOM.  
2. El programa recorre esa carpeta y **carga cada archivo DICOM** usando la librería `pydicom`.  
3. Para cada archivo, se **extraen metadatos relevantes**, como:
   - Identificador del paciente (`PatientID`).  
   - Nombre del paciente (`PatientName`).  
   - Identificador único del estudio (`StudyInstanceUID`).  
   - Descripción del estudio (`StudyDescription`).  
   - Fecha del estudio (`StudyDate`).  
   - Modalidad de la imagen (`Modality`, por ejemplo CT, MR, etc.).  
   - Número de filas (`Rows`) y columnas (`Columns`) de la imagen.
4. Con ayuda de `numpy`, se accede a la matriz de píxeles (`pixel_array`) y se **calcula la intensidad promedio** de cada imagen. Este valor se agrega como una nueva columna llamada **`IntensidadPromdio`** en el DataFrame.  
5. Toda la información se organiza en un **DataFrame de `pandas`**, donde cada fila representa un archivo DICOM y cada columna representa un metadato o resultado calculado.  
6. Finalmente, el DataFrame se **exporta a un archivo CSV**, que funciona como una pequeña base de datos tabular para análisis posteriores.

En resumen, el proyecto integra conceptos de bioingeniería, informática médica y programación en Python para automatizar tareas básicas de un flujo PACS: lectura de estudios, organización de metadatos y análisis inicial de las imágenes.


# 2: Explica brevemente por qué DICOM y HL7 son cruciales para la interoperabilidad en salud y en qué se diferencian conceptualmente

En informática médica, la **interoperabilidad** es la capacidad de que diferentes sistemas (HIS, RIS, PACS, monitores, sistemas de laboratorio, etc.) puedan intercambiar información clínica de forma segura, coherente y comprensible. En este contexto, **DICOM** y **HL7** son dos estándares fundamentales, pero cada uno se enfoca en un tipo de información distinto.

# Una pequeña descripción de los estandares mencionados:

# DICOM:

DICOM (Digital Imaging and Communications in Medicine) es el estándar orientado a:

- El **almacenamiento**, **transmisión** y **formato** de las **imágenes médicas**.  
- Manejar en un mismo archivo:
  - La **matriz de píxeles** de la imagen (los datos crudos).  
  - Una cabecera con **metadatos clínicos y técnicos**: datos del paciente, del estudio, del equipo, de la modalidad, parámetros de adquisición, etc.

Además de definir el formato de los archivos, DICOM especifica **servicios de red** (como C-STORE, C-FIND, C-MOVE) para que equipos de distintos fabricantes puedan comunicarse entre sí. Por ejemplo, un tomógrafo puede enviar sus estudios a un servidor PACS, y luego una estación de trabajo puede consultarlos sin importar la marca de cada dispositivo.

En este taller, el uso de `pydicom` refleja precisamente esa lógica: el programa lee el contenido del archivo DICOM y accede de forma estructurada a sus tags y a la matriz de la imagen.

# HL7

HL7 (Health Level Seven) es un estándar pensado para el **intercambio de información clínica y administrativa** en los sistemas de información hospitalarios. No se centra en las imágenes, sino en los **eventos clínicos** y en los datos textuales que describen lo que le pasa al paciente dentro del sistema de salud, por ejemplo:

- Admisiones, traslados y altas de pacientes.  
- Órdenes médicas (por ejemplo, “solicitar una TAC de tórax”).  
- Resultados de laboratorio (por ejemplo, un hemograma o un panel bioquímico).  
- Informes clínicos y documentos médicos.  
- Citas, procedimientos y otros eventos administrativos.

En versiones clásicas (HL7 v2.x), la información se organiza en **mensajes** compuestos por segmentos. En versiones modernas como **HL7 FHIR**, los datos se exponen como recursos web (JSON, XML) accesibles a través de servicios REST, lo que facilita su integración con aplicaciones web y móviles.

#### Diferencias conceptuales y rol en la interoperabilidad

- **Tipo de datos que representan:**
  - **DICOM:** se centra en **imágenes médicas** y sus **metadatos técnicos y clínicos**.  
  - **HL7:** se centra en la **información clínica y administrativa textual** (eventos, órdenes, resultados, documentos, etc.).

- **Nivel de uso dentro de la institución:**
  - **DICOM:** opera principalmente en el ámbito de los **equipos de imagen** y los sistemas PACS.  
  - **HL7:** opera a nivel del **sistema de información hospitalaria** (HIS, EMR, LIS, etc.) y de los flujos de trabajo clínicos.

- **Forma de representación:**
  - **DICOM:** archivos binarios DICOM y protocolos específicos del estándar.  
  - **HL7:** mensajes estructurados (v2.x) o recursos web (FHIR) que viajan entre sistemas.

Ambos son cruciales para la interoperabilidad porque se **complementan**:

- HL7 puede comunicar, por ejemplo, la **orden** de realizar un estudio de imagen a un paciente determinado.  
- DICOM se encarga de **almacenar y transmitir** las imágenes resultantes de esa orden, junto con sus metadatos.  

Gracias a estos estándares, es posible que sistemas y equipos de diferentes fabricantes trabajen juntos sin que cada institución tenga que inventar su propio formato propietario.


# 3: ¿Qué relevancia clínica o de pre-procesamiento podría tener el análisis de la distribución de intensidades en una imagen médica?

Analizar la **distribución de intensidades** de una imagen médica (por ejemplo, mediante un histograma) es importante por varios motivos, tanto clínicos como técnicos.

#### Relevancia clínica

1. **Diferenciación de tejidos y estructuras**  
   En modalidades como la tomografía computarizada (CT), los niveles de intensidad se relacionan con las densidades de los tejidos (por ejemplo, unidades Hounsfield). La forma del histograma —sus picos, su anchura y su posición— da una idea de qué tejidos predominan en la imagen: aire, grasa, tejido blando, hueso, etc.

2. **Detección de lesiones o cambios patológicos**  
   Lesiones, tumores, áreas de edema, necrosis o sangrado suelen modificar la distribución normal de intensidades. La aparición de nuevos picos, “colas” o concentraciones de valores poco usuales puede indicar la presencia de regiones con propiedades distintas al tejido sano. Comparar la distribución de intensidades entre estudios sucesivos de un mismo paciente también ayuda a evaluar la respuesta al tratamiento.

3. **Evaluación de la calidad de la imagen**  
   Una imagen demasiado oscura (intensidades muy bajas) o saturada (muchos valores altos) puede indicar problemas en la dosis, en la calibración del equipo o en el protocolo de adquisición. Revisar la distribución de intensidades ayuda a identificar imágenes que podrían ser poco útiles para el diagnóstico o que requieren repetir el estudio.

#### Relevancia en el pre-procesamiento

1. **Normalización y estandarización**  
   Antes de aplicar algoritmos de segmentación o modelos de machine learning, suele ser necesario normalizar las intensidades para reducir la variabilidad entre estudios, equipos o centros. Poder observar la distribución permite elegir estrategias de normalización (recorte de percentiles, reescalado, etc.) que dejen los datos en rangos comparables.

2. **Selección de ventanas de visualización (windowing)**  
   En CT, las “ventanas” (pulmón, mediastino, hueso, etc.) dependen de rangos específicos de intensidades. Conocer la distribución ayuda a escoger los parámetros del window level y window width para resaltar correctamente las estructuras de interés.

3. **Elección de umbrales para segmentación**  
   Muchos métodos simples de segmentación se basan en umbrales de intensidad. El histograma muestra dónde se agrupan los valores y permite elegir umbrales que correspondan a clases razonables (por ejemplo, separar aire de tejido o tejido de hueso).

4. **Detección de artefactos y valores atípicos**  
   Picos extraños o valores demasiado extremos en la distribución pueden asociarse a artefactos de movimiento, metal, ruido, errores de reconstrucción, etc. Detectar estas características desde el análisis de intensidades sirve para decidir si una imagen debe ser filtrada, corregida o descartada antes de aplicar técnicas más avanzadas.

En conjunto, el análisis de la distribución de intensidades es una herramienta básica pero muy útil tanto para **interpretar clínicamente** la imagen como para **diseñar un flujo de pre-procesamiento robusto** que prepare los datos para algoritmos posteriores.


# 4: Mencionar dificultades encontradas y la importancia de las herramientas de Python para el análisis de datos médicos

# Dificultades encontradas

Al desarrollar la aplicación se identificaron varias dificultades:

1. **Archivos que no son DICOM o están dañados**  
   Al recorrer un directorio completo, es muy comun  encontrar archivos que no son DICOM o que no pueden leerse correctamente. Esto obliga a manejar excepciones al usar `pydicom.dcmread()` y a decidir qué hacer con esos archivos (por ejemplo, ignorarlos y reportarlos en consola).

2. **Metadatos faltantes por anonimización**  
   Muchos estudios de ejemplo o de investigación se distribuyen con datos de paciente parcialmente anonimizados. Esto implica que algunos tags (como `PatientName` o `PatientID`) pueden no existir o venir vacíos.Razón por la cual el código debe estar preparado para que la ausencia de estos campos no provoque errores.

3. **Acceso a la matriz de píxeles (`pixel_array`)**  
   Aunque en la mayoría de los casos se puede acceder directamente a `ds.pixel_array`, hay situaciones en las que la codificación de la imagen o la compresión generan problemas. Si eso ocurre, el programa se diseña para manejar la excepción y, por ejemplo, guardar un valor `NaN` en la intensidad promedio de esa imagen.

4. **Organización del código (POO y legibilidad)**  
   Estructurar el código en una clase (`ProcesadorDICOM`) ayuda a tener todo más ordenado (carga, extracción de metadatos, análisis, guardado), pero inicialmente puede resultar un reto pensar cómo dividir las responsabilidades entre métodos, qué atributos debe tener el objeto, y cómo mantener el código claro y legible.

5. **Gestión del entorno de trabajo y dependencias**  
   Es necesario crear un entorno virtual, instalar librerías (`pydicom`, `numpy`, `pandas`) y asegurarse de que el script funcione en cualquier equipo donde se vaya a ejecutar (en este caso, en nuestros ordenadores o en el del monitor posterirmente), pues problemas de versiones o de rutas pueden aparecer si el entorno no está bien configurado.

#### Importancia de las herramientas de Python para el análisis de datos médicos

Python se ha convertido en una herramienta muy importante en bioingeniería y análisis de datos médicos por varias razones:

- **Simplicidad de la sintaxis:**  
  Facilita que estudiantes y profesionales de la salud puedan aprender a programar sin tener que lidiar con demasiados detalles de bajo nivel.

- **Ecosistema científico muy completo:**  
  - `pydicom` permite trabajar directamente con el estándar DICOM, leer metadatos, acceder a la imagen y manipularla.  
  - `numpy` está optimizado para manejar arreglos y matrices grandes, como las imágenes médicas, y ofrece operaciones numéricas rápidas.  
  - `pandas` facilita la organización de metadatos en tablas, su filtrado, agrupación, exportación a CSV y análisis exploratorio.

- **Integración con machine learning e inteligencia artificial:**  
  Python se conecta fácilmente con librerías como `scikit-learn`, `TensorFlow`, `PyTorch` y otras, lo que permite dar el salto desde el simple análisis de metadatos hasta la construcción de modelos de clasificación, detección de patologías, segmentación, etc.

- **Software libre y comunidad activa:**  
  Al ser herramientas de código abierto, cualquier persona puede usarlas, revisarlas, adaptarlas y compartir mejoras. Esto fomenta la colaboración entre universidades, hospitales y grupos de investigación, facilita la reproducibilidad de los estudios y reduce costos de licencias.

En resumen, las herramientas de Python permiten construir, de forma relativamente sencilla, pipelines completos para el manejo y análisis de datos médicos: desde leer archivos DICOM hasta aplicar técnicas avanzadas de procesamiento de imágenes y aprendizaje automático.
