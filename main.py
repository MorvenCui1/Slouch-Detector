import cv2
import mediapipe as mp
import numpy as np

past_update = ""
current_update = ""

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle
    
    return angle

#'''
print("Welcome to posture fixer!\n")
print("Stand up straight and far enough from the camera so that your whole body is visible, and face the front of your body to the camera!\n")
print("(latest updates can take a while too load, and updates can be choppy at times due to processing rates)\n")
print("Enjoy the latest updates on your posture!\n")
go_ahead = input("Enter anything to continue: ")
print("---------------------------")
#'''

mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_pose=mp.solutions.pose

cap=cv2.VideoCapture(0)

# Setup up Mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image=cap.read()
        
        image.flags.writeable = False
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        # Make detection
        results=pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            left_hip_array  = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip_array = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            left_shoulder_array = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_shoulder_array = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            nose_array = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            left_knee_array = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_knee_array = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            # Calculate angle made with nose, shoulder, and hip
            left_angle_up = calculate_angle(nose_array, left_shoulder_array, left_hip_array)
            right_angle_up = calculate_angle(nose_array, right_shoulder_array, right_hip_array)

            # Calculate angle made with shoulder, hip, and knee
            left_angle_down = calculate_angle(left_shoulder_array, left_hip_array, left_knee_array)
            right_angle_down = calculate_angle(right_shoulder_array, right_hip_array, right_knee_array)

            '''
            #Collecting data
            print("Left Side Angle Up")
            print(left_angle_up)

            print("Right Side Angle Up")
            print(right_angle_up)
            #'''

            '''
            #Collecting data
            print("Left Side Angle Down")
            print(left_angle_down)

            print("Right Side Angle Down")
            print(right_angle_down)
            #'''

            #'''

            # Evaluate posture

            # Good posture
            if (left_angle_up >= 143 and right_angle_up >= 143 and left_angle_up <= 155 and right_angle_up <= 155):
                past_update = current_update
                current_update = "Good posture"
                if (past_update != current_update):
                    print("---------------------------")
                    print("Latest Update:")
                    print(current_update)
                    print("Keep up the good work!")
            
            # Bad posture slouching
            elif (left_angle_up <= 142 and right_angle_up <= 142):
                past_update = current_update
                current_update = "Bad posture, slouching forward"
                if (past_update != current_update):
                    print("---------------------------")
                    print("Latest Update:")
                    print(current_update)
                    print("Shoulders and head too far forward! Bring your shoulders and head backwards, and straighten your spine!")
            #'''
                
        except:
            pass

        mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('Mediapipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
mp_drawing.DrawingSpec