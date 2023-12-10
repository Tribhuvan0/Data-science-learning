from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to store connected clients
connected_clients = {}

def notify_users():
    while True:
        time.sleep(5)  # Notify users every 5 seconds
        message = f"New update at {time.strftime('%H:%M:%S')}"
        socketio.emit('notification', {'message': message}, namespace='/notifications')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/notifications')
def handle_connect():
    connected_clients[request.sid] = True
    print(f"Client {request.sid} connected")

@socketio.on('disconnect', namespace='/notifications')
def handle_disconnect():
    if request.sid in connected_clients:
        del connected_clients[request.sid]
        print(f"Client {request.sid} disconnected")

if __name__ == '__main__':
    # Start the background thread for notifications
    notification_thread = threading.Thread(target=notify_users)
    notification_thread.start()

    # Run the Flask-SocketIO app
    socketio.run(app, debug=True)
