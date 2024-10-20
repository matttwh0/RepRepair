import cv2
import mediapipe as mp
import numpy as np
import os

def process_video(video_path):
    # Initialize Mediapipe Pose model
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Load pre-recorded video
    cap = cv2.VideoCapture(video_path)
    video_title = os.path.splitext(os.path.basename(video_path))[0]

    output_folder = 'output'
    os.makedirs(output_folder, exist_ok=True)

    # Extract video title and create output path
    out_path = os.path.join(output_folder, f"{video_title}_output.mp4")

    # Define the codec and create VideoWriter object to save output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

    correct_reps = 0
    incorrect_reps = 0
    rep_started = False
    correct_rep = False
    in_session = False
    lowest_right_elbow_angle = None
    lowest_left_elbow_angle = None
    rep_data = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert the image to RGB as MediaPipe requires it
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process the image and extract pose landmarks
            results = pose.process(image)
            
            # Convert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw the pose annotation on the image
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                            
                # Extract landmarks
                landmarks = results.pose_landmarks.landmark
                
                # Get joint landmarks for lat pulldown
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                
                # Calculate elbow flare angle (angle between shoulder, elbow, and wrist)
                def calculate_angle(a, b, c):
                    a = np.array([a.x, a.y])
                    b = np.array([b.x, b.y])
                    c = np.array([c.x, c.y])
                    
                    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                    angle = np.abs(radians * 180.0 / np.pi)
                    
                    if angle > 180.0:
                        angle = 360 - angle
                    
                    return angle
                
                # Calculate angles for both elbows
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                
                # Update the lowest angles during a rep
                if rep_started:
                    if lowest_right_elbow_angle is None or right_elbow_angle < lowest_right_elbow_angle:
                        lowest_right_elbow_angle = right_elbow_angle
                    if lowest_left_elbow_angle is None or left_elbow_angle < lowest_left_elbow_angle:
                        lowest_left_elbow_angle = left_elbow_angle
                
                # Display elbow angles
                cv2.putText(image, f'R Elbow Angle: {int(right_elbow_angle)}', 
                            (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0]) - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.putText(image, f'L Elbow Angle: {int(left_elbow_angle)}', 
                            (int(left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0]) - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                
                # State determination based on elbow angles
                if 145 <= right_elbow_angle <= 180 and 145 <= left_elbow_angle <= 180:
                    # Idle state
                    wrist_color_right = (0, 0, 255)  # Red
                    wrist_color_left = (0, 0, 255)  # Red
                    in_session = False
                    if rep_started:
                        if correct_rep:
                            correct_reps += 1
                            rep_data.append(f'CorrectRep{correct_reps} = ({lowest_right_elbow_angle}, {lowest_left_elbow_angle})')
                            print(f'Correct Rep - Lowest Right Elbow Angle: {lowest_right_elbow_angle}, Lowest Left Elbow Angle: {lowest_left_elbow_angle}')
                        else:
                            incorrect_reps += 1
                            rep_data.append(f'IncorrectRep{incorrect_reps} = ({lowest_right_elbow_angle}, {lowest_left_elbow_angle})')
                            print(f'Incorrect Rep - Lowest Right Elbow Angle: {lowest_right_elbow_angle}, Lowest Left Elbow Angle: {lowest_left_elbow_angle}')
                        rep_started = False
                        correct_rep = False
                        lowest_right_elbow_angle = None
                        lowest_left_elbow_angle = None
                elif 70 < right_elbow_angle < 145 and 70 < left_elbow_angle < 145:
                    # In session state
                    wrist_color_right = (255, 0, 0)  # Blue
                    wrist_color_left = (255, 0, 0)  # Blue
                    in_session = True
                    if not rep_started:
                        rep_started = True
                        correct_rep = False
                else:
                    # Optimal state
                    right_wrist_green = 55 <= right_elbow_angle <= 70
                    left_wrist_green = 55 <= left_elbow_angle <= 70
                    if right_wrist_green and left_wrist_green:
                        wrist_color_right = (0, 255, 0)  # Green
                        wrist_color_left = (0, 255, 0)  # Green
                        correct_rep = True
                    else:
                        wrist_color_right = (255, 0, 0)  # Blue
                        wrist_color_left = (255, 0, 0)  # Blue
                
                # Display rep counts
                cv2.putText(image, f'Correct Reps: {correct_reps}', (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f'Incorrect Reps: {incorrect_reps}', (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                # Display joint points
                cv2.putText(image, 'R Shoulder', 
                            (int(right_shoulder.x * frame.shape[1]), int(right_shoulder.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, 'L Shoulder', 
                            (int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, 'R Elbow', 
                            (int(right_elbow.x * frame.shape[1]), int(right_elbow.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, 'L Elbow', 
                            (int(left_elbow.x * frame.shape[1]), int(left_elbow.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.circle(image, (int(right_wrist.x * frame.shape[1]), int(right_wrist.y * frame.shape[0])), 10, wrist_color_right, -1)
                cv2.circle(image, (int(left_wrist.x * frame.shape[1]), int(left_wrist.y * frame.shape[0])), 10, wrist_color_left, -1)
                cv2.putText(image, 'R Wrist', 
                            (int(right_wrist.x * frame.shape[1]), int(right_wrist.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, 'L Wrist', 
                            (int(left_wrist.x * frame.shape[1]), int(left_wrist.y * frame.shape[0])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Write the resulting frame to the output video
            out.write(image)

            # Display the resulting frame
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Return the rep data and the output video path
    return rep_data, out_path

# Example usage:
# rep_data, video_path = process_video('input_vid/IMG_1443.mp4')
# print(rep_data)
# print(f'Processed video saved at: {video_path}')
