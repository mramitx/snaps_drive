from flask import Flask, render_template, Response
import cv2
import requests
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# --- Telegram Bot Config ---
BOT_TOKEN = "8354022777:AAF3qM-nVuU0zvWHn71WgFP4TqYCfDo2NPA"
CHAT_ID = "1669489463"

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    cap = cv2.VideoCapture(0)
    # Wait for camera to warm up
    for _ in range(5):
        ret, frame = cap.read()
    ret, frame = cap.read()
    cap.release()

    if ret:
        _, img_encoded = cv2.imencode('.jpg', frame)
        files = {'photo': ('image.jpg', img_encoded.tobytes())}
        payload = {'chat_id': CHAT_ID}
        telegram_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
        requests.post(telegram_url, data=payload, files=files)
        return "Image sent to Telegram!"
    else:
        return "Failed to capture image", 500

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)