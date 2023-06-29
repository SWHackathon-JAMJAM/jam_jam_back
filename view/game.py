from flask import Flask, Response
from flask import Blueprint, session, redirect, url_for, render_template, request
import cv2
import pymysql
import mediapipe as mp
import random
game = Blueprint("game", __name__, url_prefix="/game")
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
menu = Blueprint("menu", __name__, url_prefix="/menu")
db = pymysql.connect(host=host, port=port, user=user,password=password, database=database)
cur = db.cursor()
# -----------------------------------------------------------------------
# Initialize MediaPipe hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)

# Randomly generate initial point coordinates
point_x = random.randint(0, 640)
point_y = 0

# Variables for moving the point
move_speed_x = 5
move_direction_x = 1
move_speed_y = 5
move_direction_y = 1

# Finger bend count initialization
finger_bend_count = [0, 0, 0, 0, 0]  # [Thumb, Index, Middle, Ring, Pinky]

# Previous finger bend status
prev_finger_bend = [False, False, False, False, False]


def generate_frames():
    global point_x, point_y, move_direction_x, move_direction_y, prev_finger_bend, move_speed_y, finger_bend_count
    prev_finger_bend = [False, False, False, False, False]  # Initialize previous finger bend status
    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Flip the frame horizontally (comment out this line if you want the original orientation)
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe
        results = hands.process(image)

        # Check if any hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get hand landmarks
                hand_landmarks_list = mp_hands.HandLandmark

                # Get the landmarks for the hand
                hand_landmark_points = []
                for landmark in hand_landmarks_list:
                    hand_landmark_points.append(hand_landmarks.landmark[landmark])

                # Get the bounding box coordinates for the hand
                x_min = int(min(hand_landmark_points, key=lambda x: x.x).x * frame.shape[1])
                x_max = int(max(hand_landmark_points, key=lambda x: x.x).x * frame.shape[1])
                y_min = int(min(hand_landmark_points, key=lambda y: y.y).y * frame.shape[0])
                y_max = int(max(hand_landmark_points, key=lambda y: y.y).y * frame.shape[0])

                # Draw the bounding box rectangle
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

                # Check if the point touches the bounding box
                if x_min <= point_x <= x_max and y_min <= point_y <= y_max:
                    # Set y-coordinate to 0
                    point_y = 0

                # Finger bend detection
                thumb_bend = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y < hand_landmarks.landmark[
                    mp_hands.HandLandmark.THUMB_TIP].y
                index_bend = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y < hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_PIP].y
                middle_bend = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y < hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
                ring_bend = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y < hand_landmarks.landmark[
                    mp_hands.HandLandmark.RING_FINGER_PIP].y
                pinky_bend = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y < hand_landmarks.landmark[
                    mp_hands.HandLandmark.PINKY_PIP].y

                # Finger bend status
                finger_bend = [thumb_bend, index_bend, middle_bend, ring_bend, pinky_bend]

                for i, bend in enumerate(finger_bend):
                    if bend and not prev_finger_bend[i]:
                        finger_bend_count[i] += 1

                prev_finger_bend = finger_bend

                # Increase move speed if finger bend count reaches 10
                if all(count >= 10 for count in finger_bend_count):
                    move_speed_y += 10
                    finger_bend_count = [0, 0, 0, 0, 0]

        # Draw a large blue point
        cv2.circle(frame, (point_x, point_y), 20, (255, 0, 0), -1)

        # Update the point coordinates
        point_x += move_speed_x * move_direction_x
        point_y += move_speed_y * move_direction_y

        # Change the move direction if the point reaches the boundary
        if point_x >= frame.shape[1] or point_x <= 0:
            move_direction_x *= -1
        if point_y >= frame.shape[0] or point_y <= 0:
            move_direction_y *= -1

        # Display finger bend count
        cv2.putText(frame, f"Thumb: {finger_bend_count[0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Index: {finger_bend_count[1]}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Middle: {finger_bend_count[2]}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Ring: {finger_bend_count[3]}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Pinky: {finger_bend_count[4]}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@game.route('/')
def index():
    if not 'id' in session:
        return redirect(url_for('web.login_name'))
    return render_template('gamepage.html')


@game.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

