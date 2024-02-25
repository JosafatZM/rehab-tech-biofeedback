import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                            )

def display_image(image):
    cv2.imshow('MediaPipe Feed', image)
    cv2.waitKey(10)
