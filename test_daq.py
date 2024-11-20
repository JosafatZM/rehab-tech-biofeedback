import nidaqmx
from nidaqmx.errors import DaqError

# Función para probar la conexión de la DAQ
def test_daq_connection():
    try:
        # Crear una tarea para probar la conexión
        with nidaqmx.Task() as task:
            # Intentar añadir un canal analógico de voltaje
            task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
            
            # Configurar la sincronización de reloj
            task.timing.cfg_samp_clk_timing(rate=2000.0)
            
            # Leer una muestra de prueba
            data = task.read(number_of_samples_per_channel=1)
            
            # Si llega aquí, la conexión fue exitosa
            print("Conexión correcta con la DAQ. Valor leído:", data)
    except DaqError as e:
        # Capturar errores específicos de la DAQ
        print("Error con la DAQ:", e)
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print("Error inesperado:", e)

# Llamar a la función de prueba
test_daq_connection()


def get_id():
    return 5

a = get_id()

print(a)