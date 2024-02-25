# Proyecto de Análisis de Movimiento con EMG y Visión Computacional

**Descripción:**

Este proyecto se focaliza en analizar el movimiento de ejercicios específicos mediante la utilización de señales electromiográficas (EMG) y un modelo de visión computacional. El objetivo principal es realizar un análisis detallado de los movimientos capturados, haciendo uso del modelo Pose de MediaPipe y la información proporcionada por el electromiograma (EMG).

Los datos de los EMG y los valores angulares capturados serán almacenados en una base de datos MySQL para su posterior análisis. Para facilitar la interpretación de estos datos, se ha desarrollado una interfaz gráfica en Python. Esta interfaz permitirá a los usuarios consultar gráficas de los registros y obtener archivos de texto (txt) con los mismos para un análisis más detallado.

## Componentes principales:

**Captura de datos:**
  * EMG: Se utiliza un sensor EMG para capturar la actividad muscular durante el ejercicio.
  * Visión computacional: Se utiliza el modelo Pose de MediaPipe para obtener los valores angulares de las articulaciones del cuerpo.
    
**Almacenamiento de datos:**
  * Los datos de EMG y los valores angulares capturados se almacenarán en una base de datos MySQL.
    
**Interfaz gráfica:**
  * Se ha desarrollado una interfaz gráfica usando la libreria CustomTKInter de Python para consultar y visualizar los registros de forma intuitiva. Esta interfaz permitirá a los usuarios:
    * Consultar gráficas de los registros.
    * Obtener archivos de texto (txt) con los datos para un análisis más detallado.

## Planes Futuros:
* **Mejora de la Interfaz Gráfica:** Agregar funcionalidades adicionales para mejorar la experiencia del usuario y la visualización de datos.
* **Implementación de Funcionalidades de Exportación:** Desarrollar la capacidad de exportar datos en diferentes formatos para facilitar su uso en otras herramientas y plataformas.
* **Optimización del Rendimiento:** Realizar ajustes y optimizaciones para mejorar la velocidad y eficiencia del sistema, especialmente en el procesamiento de datos en tiempo real.

**Nota:** Este README está diseñado para un proyecto aún en desarrollo. Se actualizará a medida que el proyecto avance.

## Recursos adicionales:

* **Documentación de MediaPipe Pose:** [https://google.github.io/mediapipe/solutions/pose.html](https://google.github.io/mediapipe/solutions/pose.html)
* **Documentación de CustomTKInter:** [https://github.com/TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
