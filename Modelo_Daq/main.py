from .calculate_pose.pose_utils import calculate_angles
from .visualization.visualization import draw_landmarks, display_image
from .data_aqcuisition import data_aqcuisition as daq

# computational vision librarie
import cv2
# to use mediapipe solutions
import mediapipe as mp
# to work with trigonometrycs
import numpy as np 
# some time calculations
import time
# connect with mysql database


def modelo_daq():

    data_channel1 = []
    data_channel2 = []
    data_channel3 = []

    data_emg = daq.DAQ(channel1= data_channel1,
                    channel2= data_channel2,
                    channel3= data_channel3)

    # to use drawing utils
    mp_drawing = mp.solutions.drawing_utils
    # to use pose utils (most specifically pose estimation)
    mp_pose = mp.solutions.pose

    # Video 
    # rep count 
    cont_SEW_l = 0
    cont_SEW_r = 0

    correct_pose = False
    serie1 = True

    # angle arrays
    left_sew_angles = []
    right_sew_angles = []
    left_hse_angles = []
    right_hse_angles = []



    bandera_inicio = True



    # the camera assigned to a variable '(number x) represents the no. of device'

    # # to use computer's camera 
    # cap = cv2.VideoCapture(0)

    # to use Alan's camera
    cap = cv2.VideoCapture(0)

    # Setup mediapipe instance 
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:


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

                #pop-up angle
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
                                
                                correct_pose = True
                                    
                                if cont_SEW_l <= 0 and cont_SEW_r <= 0 and bandera_inicio:
                                    try:
                                        start_daq_time = time.time()
                                        data_emg.daq_thread()
                                        bandera_inicio = False
                                        
                                    except:
                                        print("chale :(")

                                    start_time = time.time()
                                    print("comienza la serie ")
                                    pass

                # Saving angles        
                if correct_pose and serie1:
                    # saving angles into arrays
                    left_sew_angles.append(angle_SEW_left)
                    right_sew_angles.append(angle_SEW_right)
                    left_hse_angles.append(angle_HSE_left)
                    right_hse_angles.append(angle_HSE_right)   
                

                # Curl count
                if angle_SEW_left < 70 and angle_HSE_left >= 80 and correct_pose:
                    stage_sew_l = 'Down'
                if angle_SEW_left > 84 and stage_sew_l == 'Down' and angle_HSE_left >= 80:
                    stage_sew_l = 'Up'
                    cont_SEW_l += 1
                    print(F"{cont_SEW_l}")
                

                if angle_SEW_right < 70 and angle_HSE_right >= 80 and correct_pose:
                    stage_sew_r = 'Down'
                if angle_SEW_right > 84 and stage_sew_r == 'Down' and angle_HSE_right >= 80:
                    stage_sew_r = 'Up'
                    cont_SEW_r += 1
                
                
                # to know the end of a series
                if cont_SEW_r == 12 or cont_SEW_l == 12:
                    
                    correct_pose = False
                    final_time = time.time()
                    
                    # restart reps counters
                    cont_SEW_r = 0
                    cont_SEW_l = 0

                    # upload data into a MySQL database
                    if serie1:
                        # Función para detener el hilo de adquisición de datos
                        data_emg.stop_daq_thread()
                        print(f"len DAQ: {len(data_channel1)}")
                        print(f"len angulos: {len(left_hse_angles)} ")
                        print(f"Tiempo de la serie: {final_time - start_time}")
                        print(f"Tiempo de la DAQ: {final_time - start_daq_time}")
                        print(f"fs angulos: {len(left_hse_angles)/ (final_time - start_daq_time)}")
                        break

            except:
                pass

            draw_landmarks(image, results)
            display_image(image)
            

            # to close down our video feed 
            if cv2.waitKey(10) & 0xFF == ord('E'):
                break
            # 0xFF is checking for what key we hit on our keyboard

        # release our camera/ webcam
        cap.release()
        # I think it's kinda obvious what this does 
        cv2.destroyAllWindows()