#Super busted and using as a proof of concept 
import cv2
import numpy as np
import pyautogui
from flask import Flask, render_template, request, Response, jsonify, send_file
import mss
import socket
import os

app = Flask(__name__)

# Global variables for storing the received frame and clipboard text
current_frame = None
remote_ip = 'REMOTE_COMPUTER_IP'  # Default IP, replace with your IP..
clipboard_text = ''

# Function to capture the screen
def capture_screen():
    with mss.mss() as sct:
        screen = sct.shot(output='screen.jpg')
        return cv2.imread(screen)

@app.route('/')
def index():
    return render_template('index.html', remote_ip=remote_ip, clipboard_text=clipboard_text)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    global current_frame
    while True:
        frame = capture_screen()
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        jpg_frame = cv2.imencode('.jpg', current_frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_frame + b'\r\n')

@app.route('/control', methods=['POST'])
def control():
    global remote_ip
    global clipboard_text
    action = request.form.get('action')
    if action == 'click':
        pyautogui.click()
    elif action == 'scrollup':
        pyautogui.scroll(1)
    elif action == 'scrolldown':
        pyautogui.scroll(-1)
    elif action == 'quit':
        return jsonify({"message": "Quitting"})
    elif action == 'set_ip':
        remote_ip = request.form.get('ip_address')
    elif action == 'get_clipboard':
        return jsonify({"clipboard_text": clipboard_text})
    elif action == 'set_clipboard':
        clipboard_text = request.form.get('clipboard_text')
        return 'Clipboard updated successfully'
    return jsonify({"message": "Action executed"})

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        return 'File uploaded successfully'
    else:
        return 'No file selected'

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

if __name__ == "__main__":
    # Create the 'uploads' directory for file storage
    os.makedirs('uploads', exist_ok=True)
    
    app.run(host='0.0.0.0', port=8080)
