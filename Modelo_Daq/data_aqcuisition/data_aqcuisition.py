import nidaqmx
import threading


class DAQ:
    
    detener_daq_thread = False

    def __init__(self, channel1, channel2, channel3):
        self.channel1 = channel1
        self.channel2 = channel2
        self.channel3 = channel3
    
    def daq_thread(self):
        thread_instance = threading.Thread(target=self.daq)
        thread_instance.start()
        
    def daq(self):
        
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:2")
            task.timing.cfg_samp_clk_timing(rate=2000.0)
            
            while not DAQ.detener_daq_thread:
            
                data = task.read(number_of_samples_per_channel=1)
                self.channel1.append(data[0][0])
                self.channel2.append(data[1][0])
                self.channel3.append(data[2][0])

    @classmethod
    def stop_daq_thread(cls):
        # Define un método de clase para detener el hilo de DAQ
        cls.detener_daq_thread = True
        print("cambio")

