import numpy as np

def calculate_angles(first, middle, last):
    first = np.array(first)
    middle = np.array(middle)
    last = np.array(last)

    radians = np.arctan2(last[1] - middle[1], last[0] - middle[0]) - np.arctan2(first[1] - middle[1], first[0] - middle[0])
    angle = np.abs(radians * 180 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    
    return angle
