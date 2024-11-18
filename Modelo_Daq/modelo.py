import cv2
# to use mediapipe solutions
import mediapipe as mp
# to work with trigonometrycs
import numpy as np 
# some time calculations
import matplotlib.pyplot as plt

def modelo():
    print("Test de postura iniciando... ")

    # to use drawing utils
    mp_drawing = mp.solutions.drawing_utils
    # to use pose utils (most specifically pose estimation)
    mp_pose = mp.solutions.pose

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

                cv2.putText(image, str(round(angle_HSE_right, 2)),
                tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)

                # Escribir el texto encima (verde)
                cv2.putText(image, str(round(angle_HSE_right, 2)),
                            tuple(np.multiply(shoulder, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                
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
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(image, str(round(angle_SEW_right, 2)),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,cv2.LINE_AA
                            )
        

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
            if final_ad or cv2.waitKey(10) & 0xFF == ord('E'):
                break
            # 0xFF is checking for what key we hit on our keyboard

        # release our camera/ webcam
        cap.release()
        # I think it's kinda obvious what this does 
        cv2.destroyAllWindows()