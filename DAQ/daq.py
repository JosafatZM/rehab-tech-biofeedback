import nidaqmx

def daq_instance(data_channel1, data_channel2, data_channel3):
    with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:2")
            # sampling frequency
            task.timing.cfg_samp_clk_timing(rate=1000.0)
            
            
            while True:
                data = task.read(number_of_samples_per_channel=1)
                
                data_channel1.append(data[0][0])
                data_channel2.append(data[1][0])
                data_channel3.append(data[2][0])