from DAQ.daq import daq_instance

import time
import cv2
import numpy as np
import threading
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def modelo():
    # Video 
    # rep count 
    cont_SEW_l = 0
    cont_SEW_r = 0
    cont = 0 
    # rep stage
    stage = None
    correct_pose = False
    bandera_timer = False
    serie2 = False
    serie1 = True

    # angle arrays
    left_sew_angles = []
    right_sew_angles = []
    left_hse_angles = []
    right_hse_angles = []

    # emg values arrays
    data_channel1 = [] 
    data_channel2 = [] 
    data_channel3 = []


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
        
        return angle

    # the camera assigned to a variable '(number x) represents the no. of device'

    # # to use computer's camera 
    # cap = cv2.VideoCapture(0)

    # to use Alan's camera
    cap = cv2.VideoCapture(0)

    # Definir la resolución deseada
    width = 320  
    height = 240  

    # Define the desired resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Setup mediapipe instance 
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        try:
            inicio_daq = time.time()
            DAQ_thread_instance = threading.Thread(target= daq_instance())
            DAQ_thread_instance.start()
            
        except:
            print("chale :(")


        while cap.isOpened():
            
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

                # Hip, Shoulder, Elbow Left angle

                # creating this variables to pass them as arguments in the function below
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x , 
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                
                # calculate angle 
                angle_HSE_left = calculate_angles(hip, shoulder, elbow)

                # pop-up angle
                cv2.putText(image, str(round(angle_HSE_left, 2)),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )
                
                # Hip, Shoulder, Elbow Right angle

                # creating this variables to pass them as arguments in the function below
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, 
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x , 
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, 
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                
                # calculate angle 
                angle_HSE_right = calculate_angles(hip, shoulder, elbow)

                # pop-up angle
                cv2.putText(image, str(round(angle_HSE_right, 2)),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )
                

                # Shoulder, Elbow, Wrist Left angle

                # creating this variables to pass them as arguments in the function below
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x , 
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # calculate angle 
                angle_SEW_left = calculate_angles(shoulder, elbow, wrist)

                # pop-up angle
                cv2.putText(image, str(round(angle_SEW_left, 2)),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
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

                # calculate angle 
                angle_SEW_right = calculate_angles(shoulder, elbow, wrist)

                # pop-up angle
                cv2.putText(image, str(round(angle_SEW_right, 2)),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )
            

                # Check condition and display pop-up for posture 
                if angle_HSE_right < 80 or angle_HSE_left < 80:
                    # Set font and text
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = "Coloca una postura adecuada"
                    font_scale = 1
                    thickness = 2

                    # Get text size
                    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

                    # Calculate coordinates for background rectangle
                    x = int((image.shape[1] - text_size[0]) / 2)
                    y = int((image.shape[0] - text_size[1]) / 2)
                    w = text_size[0]
                    h = text_size[1]
                    padding = 10
                    bg_rect = (x - padding, y - padding, w + 2 * padding, h + 2 * padding)

                    # Draw background rectangle and text
                    cv2.rectangle(image, bg_rect, (0, 0, 255), -1, cv2.LINE_AA)
                    cv2.putText(image, text, (x, y + text_size[1]), 
                                font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

            

                # Curl count

                # Make sure the body is on a correct pose for the states

                if angle_HSE_right >= 80 and angle_HSE_right <= 120:
                    if angle_HSE_left >= 80 and angle_HSE_left <= 120:
                        if angle_SEW_right >= 155 and angle_SEW_right <= 180:
                            if angle_SEW_left >= 155  and angle_SEW_left <= 180:
                                stage = 'Correcto'
                                correct_pose = True
                                if cont_SEW_l <= 0 and cont_SEW_r <= 0:
                                    start_time = time.time()
                                    print("comienza la serie ")
                                    pass
                                
                    
                # Make sure the arm is flexed
            
                # Curl count
                if angle_SEW_left < 70 and angle_HSE_left >= 80 and correct_pose:
                    stage_sew_l = 'Down'
                if angle_SEW_left > 84 and stage_sew_l == 'Down' and angle_HSE_left >= 80:
                    stage_sew_l = 'Up'
                    cont_SEW_l += 1
                

                if angle_SEW_right < 70 and angle_HSE_right >= 80 and correct_pose:
                    stage_sew_r = 'Down'
                if angle_SEW_right > 84 and stage_sew_r == 'Down' and angle_HSE_right >= 80:
                    stage_sew_r = 'Up'
                    cont_SEW_r += 1
                


                if correct_pose and serie1:
                    # saving angles into arrays
                    left_sew_angles.append(angle_SEW_left)
                    right_sew_angles.append(angle_SEW_right)
                    left_hse_angles.append(angle_HSE_left)
                    right_hse_angles.append(angle_HSE_right)

                    

                # to know the end of a series
                if cont_SEW_r == 12 or cont_SEW_l == 12:
                    stage = None
                    correct_pose = False
                    bandera_timer = True
                    final_time = time.time()
                    
                    # restart reps counters
                    cont_SEW_r = 0
                    cont_SEW_l = 0

                    # upload data into a MySQL database
                    if serie2:
                        pass

                    elif serie1:
                        # print(f"len DAQ: {len(data_channel1)}")
                        print(f"len angulos: {len(left_hse_angles)} ")
                        print(f"Tiempo de la serie: {final_time - start_time}")
                        print(f"Tiempo de la DAQ: {final_time - inicio_daq}")
                        break


                
                if bandera_timer is True:
                    clock_start_time = time.time()
                    elapsed_time = 0
                    

                    if serie2:
                        while elapsed_time < 60:
                            elapsed_time = time.time() - clock_start_time
                            time_left = int(60 - elapsed_time)
                        # End of the program message

                            # Set font and text for the second message
                            text2 = "Gracias por tu participacion!!"
                            text_size2, _ = cv2.getTextSize(text2, font, font_scale, thickness)

                            # Calculate coordinates for background rectangle for the second message
                            x2 = int((image.shape[1] - text_size2[0]) / 2)
                            y2 = bg_rect[1] + bg_rect[3] + padding
                            w2 = text_size2[0]
                            h2 = text_size2[1]
                            bg_rect2 = (x2 - padding, y2 - padding, w2 + 2 * padding, h2 + 2 * padding)
                            # black backgound for the timer
                            black_image = np.zeros_like(image)
                            # Draw background rectangle and text for the second message
                            cv2.rectangle(black_image, bg_rect2, (0, 255, 0), -1, cv2.LINE_AA)
                            cv2.putText(black_image, text2, (x2, y2 + text_size2[1]), 
                                        font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                            
                            cv2.imshow('MediaPipe Feed', black_image)
                            cv2.waitKey(1)
                            bandera_timer = False
                            # to close down our video feed 
                            if cv2.waitKey(10) & 0xFF == ord('E'):
                                break

                    else:
                        # ---- Timer -----
                        while elapsed_time < 60:
                            serie2 = True
                            elapsed_time = time.time() - clock_start_time
                            time_left = int(60 - elapsed_time)
                            
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
                            cv2.putText(black_image, f'Fin Serie 1, Descanso: {time_left} s', (x, y + text_size[1]), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                            
                            cv2.imshow('MediaPipe Feed', black_image)
                            cv2.waitKey(1)
                            
                            bandera_timer = False
                            stage = None
                            # to close down our video feed 
                            if cv2.waitKey(10) & 0xFF == ord('E'):
                                break
                    
                

            except:
                pass

            



            # Render my detections - Draws the landmarks and the connections on the image.
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                                    )


            # gives a pop-up of the camera 
            cv2.imshow('MediaPipe Feed', image)

            # to close down our video feed 
            if cv2.waitKey(10) & 0xFF == ord('E'):
                break
            # 0xFF is checking for what key we hit on our keyboard

        # release our camera/ webcam
        cap.release()
        # I think it's kinda obvious what this does 
        cv2.destroyAllWindows()
