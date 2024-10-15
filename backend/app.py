from flask import Flask, Response, jsonify
import cv2
import numpy as np
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

cap = None
video_started = False


def generate_video_feed():
    global cap, video_started
    feature_params = dict(maxCorners=100, qualityLevel=0.6,
                          minDistance=25, blockSize=9)
    screen_height = 480
    threshold_y = screen_height - 20
    fgbg = cv2.createBackgroundSubtractorMOG2()
    balls_entered = 0
    additional_counter = 0
    previous_time = time.time()
    previous_balls_entered = 0
    check_interval = 0.8
    increase_threshold = 13

    if not cap or not cap.isOpened():  # Re-initialize the camera if it's not open
        cap = cv2.VideoCapture(0)

    while video_started:
        ret, frame = cap.read()
        if not ret:
            break

        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(
            fgmask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_tennis_ball = np.array([20, 100, 100], dtype=np.uint8)
        upper_tennis_ball = np.array([40, 255, 255], dtype=np.uint8)
        tennis_ball_mask = cv2.inRange(
            hsv_frame, lower_tennis_ball, upper_tennis_ball)
        fgmask = cv2.bitwise_and(fgmask, tennis_ball_mask)

        detected_balls = cv2.goodFeaturesToTrack(
            fgmask, mask=None, **feature_params)

        if detected_balls is not None:
            detected_balls = np.int0(detected_balls)
            for ball in detected_balls:
                x, y = ball.ravel()
                if y >= threshold_y:
                    balls_entered += 1
                cv2.circle(frame, (x, y), 25, (255, 0, 0), 2)

        current_time = time.time()
        time_elapsed = current_time - previous_time
        if time_elapsed >= check_interval:
            if (balls_entered - previous_balls_entered) > increase_threshold:
                additional_counter += 1
            previous_time = current_time
            previous_balls_entered = balls_entered

        text = f'Balls Entered: {balls_entered}, Additional Counter: {additional_counter}'
        cv2.putText(frame, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/start_video', methods=['POST'])
def start_video():
    global video_started, cap
    if not video_started:
        video_started = True
        cap = cv2.VideoCapture(0)  # Re-initialize the camera
    return jsonify({"status": "Video started"})


@app.route('/stop_video', methods=['POST'])
def stop_video():
    global video_started, cap
    video_started = False
    if cap:
        cap.release()  # Release the camera when stopped
    return jsonify({"status": "Video stopped"})


@app.route('/video_feed')
def video_feed():
    if video_started:
        return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return jsonify({"status": "Video not started"})


if __name__ == '__main__':
    app.run(debug=True)
