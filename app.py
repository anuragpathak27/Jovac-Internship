from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/room', methods=['POST'])
def room():
    room_id = request.form.get('room_id')
    return redirect(url_for('room_page', room_id=room_id))

@app.route('/room/<room_id>')
def room_page(room_id):
    return render_template('room.html', room_id=room_id)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{username} has joined the room."}, room=room)
    emit('new_peer', {'username': username}, room=room, include_self=False)

@socketio.on('offer')
def on_offer(data):
    room = data['room']
    emit('offer', data, room=room, include_self=False)

@socketio.on('answer')
def on_answer(data):
    room = data['room']
    emit('answer', data, room=room, include_self=False)
    

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('user_left', {'username': username}, room=room)
    emit('message', {'msg': f"{username} has left the room."}, room=room)

@socketio.on('ice-candidate')
def on_ice_candidate(data):
    room = data['room']
    emit('ice-candidate', data, room=room, include_self=False)
    
@socketio.on('message')
def on_message(data):
    room = data['room']
    emit('message', data, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
