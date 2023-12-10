from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Simulated data to be updated in real-time
data = {'value': 0}

# Function to update data in the background
def background_thread():
    while True:
        time.sleep(1)
        data['value'] = random.randint(1, 100)
        socketio.emit('update_data', {'value': data['value']}, namespace='/test')

@app.route('/')
def index():
    return render_template('index.html', initial_data=data['value'])

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('update_data', {'value': data['value']})

if __name__ == '__main__':
    # Start the background thread for updating data
    bg_thread = threading.Thread(target=background_thread)
    bg_thread.start()

    # Run the Flask-SocketIO app
    socketio.run(app, debug=True)
