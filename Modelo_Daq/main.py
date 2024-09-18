import nidaqmx
# to work with data strutures
import pandas as pd
# computational vision librarie
import cv2
# to use mediapipe solutions
import mediapipe as mp
# to work with trigonometrycs
import numpy as np 
# some time calculations
import time
# graphs 
import matplotlib.pyplot as plt
# connect with mysql database
import threading  # Importa la biblioteca threading

def modelo_daq():

    # to use drawing utils
    mp_drawing = mp.solutions.drawing_utils
    # to use pose utils (most specifically pose estimation)
    mp_pose = mp.solutions.pose

    detener_daq_thread = False

    # defining a function to calculate the angle between joints 
    def calculate_angles(first, middle, last):
        first = np.array(first)
        middle = np.array(middle)
        last = np.array(last)

        # coordinates_array [x, y, z]
        # coordinates_array[0] = x
        # coordinates_array[1] = y
        # coordinates_array[2] = z

        radians = np.arctan2(last[1] - middle[1], last[0] - middle[0]) - np.arctan2(first[1] - middle[1], first[0] - middle[0])
        angle = np.abs( radians * 180 / np.pi)

        if angle > 180.0:
            angle = 360 - angle
        
        return round(angle, 3)


    def daq_thread_instance():

        global detener_daq_thread

        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
            task.timing.cfg_samp_clk_timing(rate=2000.0)
            
            
            while not detener_daq_thread:
                data = task.read(number_of_samples_per_channel=1)
            
                data_channel1.append(data[0])

    # Función para detener el hilo de adquisición de datos
    def stop_daq_thread():
        global detener_daq_thread
        detener_daq_thread = True

    

    cont_SEW_r = 0
    cont = 0 
    stage = None
    bandera = False
    bandera_timer = False
    data_channel1 = []
    bandera_time = 0
    relacion_ang_time_codo = {}
    relacion_ang_time_hombro = {}
    # Set font and text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    text = "hola"
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)



    # the camera assigned to a variable '(number x) represents the no. of device'

    # # to use computer's camera 
    # cap = cv2.VideoCapture(0)

    # to use Alan's camera
    cap = cv2.VideoCapture(0)

    # Setup mediapipe instance 
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            global final_ad
            final_ad = False
            
            # camera feedback
            ret, frame = cap.read()

            # Detection and renderitation 

            # Recolor image / Reorderting - because cv2 gives us the images in BGR 
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # saving memory for when I pass this into my pose stimation model
            image.flags.writeable = False 

            # Detection
            results = pose.process(image)

            # Back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # LandMarks
            try:
                landmarks = results.pose_landmarks.landmark

                # # ----- COORDINATES ------

                # Hip, Shoulder, Elbow Right angle
                # creating this variables to pass them as arguments in the function below
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x , 
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                
                # calculate angle function
                angle_HSE_right = calculate_angles(hip, shoulder, elbow)

                # pop-up angle
                cv2.putText(image, str(round(angle_HSE_right, 2)),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )
                
                # Shoulder, Elbow, Wrist Right angle
                # creating this variables to pass them as arguments in the function below
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x , 
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, 
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # calculate angle function
                angle_SEW_right = calculate_angles(shoulder, elbow, wrist)

                # pop-up angle
                cv2.putText(image, str(round(angle_SEW_right, 2)),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )

                # Curl count
                # Make sure the body is on a correct pose for the states
                if angle_HSE_right >= 80 and angle_HSE_right <= 120:           
                    if angle_SEW_right >= 155 and angle_SEW_right <= 180:
                        stage = 'Incial'
                        bandera = True
                        
                                
                if angle_HSE_right >= 80 and angle_HSE_right <= 120:
                    if angle_SEW_right >= 131 and angle_SEW_right <= 154:
                            
                        if stage == 'Inicial':
                            stage = 'Bajada'
                        elif stage == 'Concentrica':
                            stage = 'Subida'
                                

                if angle_HSE_right >= 80 and angle_HSE_right <= 120:
                    if angle_SEW_right >= 30 and angle_SEW_right <= 130:
                        
                        stage = 'Concentrica'


                    
                # Make sure the arm is flexed
                if angle_SEW_right < 70 and angle_HSE_right >= 80 and bandera:
                    stage_sew_r = 'Down'
                if angle_SEW_right > 84 and stage_sew_r == 'Down' and angle_HSE_right >= 80:
                    stage_sew_r = 'Up'
                    cont_SEW_r += 1
                
        

                if bandera_time == 0:

                    start_time = time.time()
                    print('corriendo tiempo')
                    bandera_time = bandera_time + 1

                # screating an angle-time relation into a dict
                relacion_ang_time_codo[round(time.time() - start_time, 3)] = angle_SEW_right
                relacion_ang_time_hombro[round(time.time() - start_time, 3)] = angle_HSE_right
                
                # to know the end of a series
                if cont_SEW_r == 12:
                    final_time = time.time()
                    bandera_timer = True
                    # calculate the duration of a series
                    serie_time = final_time - start_time
                    # save times into an array
                    print(f'fin del tiempo, la serie duro: {serie_time}')
                    print("datos subidos ...")
                    
                    # cargar_datos(left_hse_angles, right_hse_angles, left_sew_angles, 
                    #              right_sew_angles, series_times[0] )

                
                if bandera_timer is True:
                    clock_start_time = time.time()
                    elapsed_time = 0
                    
                    # ---- Timer -----
                    while elapsed_time < 10:
                        elapsed_time = time.time() - clock_start_time
                        time_left = int(10 - elapsed_time)
                        
                        # Calculate coordinates for background rectangle
                        x = int((image.shape[1] - text_size[0]) / 2)
                        y = int((image.shape[0] - text_size[1]) / 2)
                        w = text_size[0]
                        h = text_size[1]
                        padding = 10
                        bg_rect = (x - padding, y - padding, w + 2 * padding, h + 2 * padding)
                        # black backgound for the timer
                        black_image = np.zeros_like(image)
                        # Draws a red rectangle for the timer
                        cv2.rectangle(black_image, bg_rect, (0, 0, 255), -1, cv2.LINE_AA)
                        # timer
                        cv2.putText(black_image, f'Descanso: {time_left} s', (x, y + text_size[1]), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        
                        cv2.imshow('MediaPipe Feed', black_image)
                        cv2.waitKey(1)
                        
                        # to close down our video feed 
                        if time_left == 1:
                        
                            final_ad = True
                            
                            break
                
                

            except:
                pass

            # Render Curl Cont

            # to draw a rectangle in our camera\ webcam window
            # (image, coord sup left, coord inf right, color)
            """
            (0,0)                         (ancho, 0)
                +-----------------------------+
                |                             |
                |                             |
                |                             |
                |                             |
                |                             |
                |                             |
                |                             |
                |                             |
                |                             |
                +-----------------------------+
            (0, altura)                (ancho, altura)
            """
            cv2.rectangle(image, (0, 0), (100, 60), (255, 255, 255), -1)
            # Rep & Stage data pop-up
            # putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
            
            # Rep datA
            cv2.putText(image, 'R-ARM-REPS', (20,55), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(cont_SEW_r), 
                        (40, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1,  (0,0,0), 2, cv2.LINE_AA)



            # Render my detections - Draws the landmarks and the connections on the image.
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                                    )


            # gives a pop-up of the camera 
            cv2.imshow('MediaPipe Feed', image)

            # to close down our video feed 
            if final_ad or cv2.waitKey(10) & 0xFF == ord('E'):
                break
            # 0xFF is checking for what key we hit on our keyboard

        # release our camera/ webcam
        cap.release()
        # I think it's kinda obvious what this does 
        cv2.destroyAllWindows()

        print(f"fs angulos: {len(relacion_ang_time_codo) /serie_time}")

    